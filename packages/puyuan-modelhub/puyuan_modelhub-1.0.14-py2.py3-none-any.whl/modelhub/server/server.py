import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

from fastapi import FastAPI, Response, Request, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated, List, Literal, Union, Dict

from modelhub.server.models.base import TextGenerationOutput, TextGenerationStreamOutput
from modelhub.server.utils import hash_password
from modelhub.server.models.errors import *
from modelhub.common.types import ErrorMessage
from modelhub.server.llm_provider import ModelProvider, ModelList

from sse_starlette.sse import EventSourceResponse
import yaml
import pymongo as pm
import uuid
import datetime
import os
import uvicorn
import hashlib
import logging
from contextlib import asynccontextmanager
import torch

from openai.types.chat import (
    CompletionCreateParams,
    ChatCompletion,
    ChatCompletionMessageParam,
)
from openai.types.chat import (
    completion_create_params,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from openai._types import NotGiven, NOT_GIVEN
from openai.types.audio import Transcription, TranscriptionCreateParams
from .utils import log_to_db, log_to_db_modelhub
from .modelhub_types import AuthParams, ChatParams, EmbeddingParams


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# setup app
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""fast api app"""
g_model_provider = None
"""model provider"""
g_mongo_db = None


def validate_global_vars():
    """Validate global variables"""
    global g_model_provider, g_mongo_db
    if not g_model_provider:
        g_model_provider = ModelProvider(
            yaml.safe_load(open(os.environ["LLM_CONFIG"]).read())
        )
    if not g_mongo_db:
        mongo_client = pm.MongoClient(os.environ["MONGO_URL"])
        g_mongo_db = mongo_client[os.environ["MONGO_DB"]]


def check_user_auth(params: AuthParams | None):
    """Check user authentication"""
    global g_mongo_db
    validate_global_vars()
    users_collection = g_mongo_db[os.environ["USERS_COLLECTION"]]
    if not params:
        return False
    hashed_password = hash_password(params.user_password)
    user = users_collection.find_one({"_id": params.user_name})
    if not user:
        return False
    return user["password"] == hashed_password


def get_auth_params(request: Request):
    """Get auth params"""
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth:
        return None
    auth = auth.replace("Bearer ", "")
    if len(auth.split(":", 1)) != 2:
        return None
    user_name, user_password = auth.split(":", 1)
    return AuthParams(user_name=user_name, user_password=user_password)


@app.middleware("http")
async def validate_token(request: Request, call_next):
    """Validate token"""
    authorized = check_user_auth(get_auth_params(request))
    if not authorized:
        return Response(status_code=401, content="Unauthorized")
    validate_global_vars()
    return await call_next(request)


@app.get("/v1/models", response_model=ModelList)
async def list_models():
    global g_model_provider
    return g_model_provider.list_models()


@app.post("/v1/audio/transcriptions")
async def transciption(
    file: Annotated[UploadFile, File()],
    model: Annotated[str, Form()],
    language: Annotated[Optional[str], Form()] = None,
    temperature: Annotated[Optional[float], Form()] = None,
):
    global g_model_provider
    print(file.filename)
    req = TranscriptionCreateParams(
        file=await file.read(), model=model, language=language, temperature=temperature
    )
    logger.info(f"transcription request: {req['model']}, {file.filename}")
    model = g_model_provider.provide(model)
    text = model.transcribe(req)
    return Transcription(text=text)


from openai.types.embedding import Embedding
from openai.types.embedding_create_params import EmbeddingCreateParams


@app.post("/v1/embeddings")
async def embeddings(params: EmbeddingCreateParams):
    global g_model_provider
    try:
        model = g_model_provider.provide(params["model"])
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")
    try:
        res = model.get_embeddings_openai(params)
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to embedding: {e}")
    return res


from typing_extensions import TypedDict


class RequestParams(TypedDict, total=False):
    messages: List[ChatCompletionMessageParam]
    model: str
    frequency_penalty: Optional[float]
    function_call: Optional[completion_create_params.FunctionCall]
    functions: Optional[List[completion_create_params.Function]]
    logit_bias: Optional[Dict[str, int]]
    max_tokens: Optional[int]
    n: Optional[int]
    presence_penalty: Optional[float]
    response_format: Optional[completion_create_params.ResponseFormat]
    seed: Optional[int]
    stop: Optional[Union[str, List[str]]]
    stream: Optional[bool]
    temperature: Optional[float]
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam]
    tools: Optional[List[ChatCompletionToolParam]]
    top_p: Optional[float]
    user: Optional[str]


@app.post("/v1/chat/completions")
async def chat_completion(
    req: RequestParams,
    request: Request,
):
    global g_model_provider, g_mongo_db
    auth = get_auth_params(request)
    req["stream"] = req.get("stream", False)
    for message in req["messages"]:
        if "function_call" in message and not message["function_call"]:
            message.pop("function_call")
    logger.info(
        f"user {auth.user_name} request: {req['model']}, {req['messages'][-1]['content']}"
    )
    try:
        model = g_model_provider.provide(req["model"])
    except ModelNotFoundError as e:
        logger.error(f"model not found: {e}")
        return ErrorMessage(err_code=404, err_msg=f"model not found: {e}")

    def stream_generator():
        res = []
        try:
            for token in model.openai_chat(req):
                res.append(token)
                yield {"data": token.json()}
            log_to_db(
                g_mongo_db[os.environ["OPENAI_COLLECTION"]],
                auth.user_name,
                req["model"],
                req,
                res,
            )
        except NotImplementedError:
            logger.info("stream not implemented")
            yield ErrorMessage(err_code=500, err_msg="stream not implemented").json()

    try:
        if req["stream"] == True:
            return EventSourceResponse(stream_generator(), ping=600)
        else:
            print(req)
            res = model.openai_chat(req)
            log_to_db(
                g_mongo_db[os.environ["OPENAI_COLLECTION"]],
                auth.user_name,
                req["model"],
                req,
                res,
            )
            logger.info(f"generated result: {res.choices[0].message.content}")
            return res
    except Exception as e:
        logger.error(f"Failed to chat: {e}")
        return ErrorMessage(err_code=500, err_msg=f"Failed to chat: {e}")


@app.post("/tokens")
async def tokens(params: ChatParams):
    """Get tokens from a model"""
    # check user name and password
    global g_model_provider

    try:
        model = g_model_provider.provide(params.model)
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")

    try:
        response = model.n_tokens(params.prompt, params.parameters)
        return {"n_tokens": response, "status": "success"}
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to get tokens: {e}")


@app.post("/chat")
async def chat(params: ChatParams, request: Request):
    """Chat with a model"""
    global g_model_provider

    auth = get_auth_params(request)
    logger.info(f"user {auth.user_name} request: {params.model}")
    start_time = datetime.datetime.now()
    # load model
    try:
        model = g_model_provider.provide(params.model)
    except ModelNotFoundError as e:
        return ErrorMessage(err_code=404, err_msg=f"model not found: {e}")
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")

    async def stream_generator():
        try:
            for token in model.stream(params.prompt, params.parameters):
                yield {"data": token.json()}
            log_to_db_modelhub(
                g_mongo_db[os.environ["MESSAGES_COLLECTION"]],
                get_auth_params(request),
                params,
                token,
            )
        except Exception as e:
            yield f'"data": {ErrorMessage(err_code=500, err_msg=f"Failed to chat: {e}").json()}'

    try:
        if params.stream:
            return EventSourceResponse(stream_generator(), ping=600)
        else:
            if "image_path" in params.parameters:
                params.parameters["image_path"] = os.path.join(
                    os.environ.get("UPLOAD_DIR"), params.parameters["image_path"]
                )
            result = model.chat(params.prompt, params.parameters)
            request_time = datetime.datetime.now() - start_time
            result.details.request_time = request_time.total_seconds()
            logger.info(f"generated result: {result.json(ensure_ascii=False)}")
            log_to_db_modelhub(
                g_mongo_db[os.environ["MESSAGES_COLLECTION"]],
                get_auth_params(request),
                params,
                result,
            )
            return result
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to chat: {e}")


@app.post("/embedding")
async def embedding(params: EmbeddingParams):
    """Get embeddings from a model"""
    # check user name and password
    global g_model_provider

    try:
        model = g_model_provider.provide(params.model)
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")

    try:
        response = model.get_embeddings(params.prompt, params.parameters)
        return response
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to embedding: {e}")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(os.environ["UPLOAD_DIR"], file.filename)
        contents = await file.read()
        file_id = hashlib.md5(contents).hexdigest()
        filename = file_id + "." + file.filename.split(".")[-1]
        file_path = os.path.join(os.environ["UPLOAD_DIR"], filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        return {"status": "success", "file_path": filename}
    except Exception as e:
        return {"error": f"failed to upload: {e}"}


@app.get("/models")
async def get_models():
    """Get all models"""
    global g_model_provider
    return {"status": "success", "models": g_model_provider.models}


@app.get("/models/{model_name}")
async def get_model_supported_params(model_name: str):
    """Get supported parameters for a model"""
    global g_model_provider
    return {
        "status": "success",
        "params": g_model_provider.get_supported_params(model_name),
    }


def validate_env():
    """Validate environment variables"""
    required_envs = [
        "MONGO_URL",
        "MONGO_DB",
        "MESSAGES_COLLECTION",
        "OPENAI_COLLECTION",
        "USERS_COLLECTION",
        "LLM_CONFIG",
        "HOST",
        "PORT",
    ]
    for env in required_envs:
        if env not in os.environ:
            logger.error(f"{env} is not set")
            exit(1)


def start_server():
    """Start the server"""
    validate_env()
    try:
        validate_global_vars()
    except Exception as e:
        logger.error(f"Failed to setup: {e}")
        exit(1)
    uvicorn.run(
        "modelhub.server.server:app",
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        workers=int(os.getenv("WORKERS", 1)),
    )


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())
    logger.info("Starting server")
    start_server()
