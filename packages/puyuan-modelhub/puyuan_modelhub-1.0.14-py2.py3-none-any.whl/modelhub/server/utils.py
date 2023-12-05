import hashlib
import time
import uuid
from typing import List
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    CompletionCreateParams,
)
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice, ChoiceDelta
from pymongo.collection import Collection
from .modelhub_types import AuthParams, ChatParams
import datetime


def log_to_db(
    db: Collection,
    user_id: str,
    model_id: str,
    req: CompletionCreateParams,
    res: ChatCompletion | List[ChatCompletionChunk],
):
    """Log a request/response pair to the database."""
    try:
        if isinstance(res, ChatCompletion):
            res = res.dict()
        elif isinstance(res, list):
            res = [c.dict() for c in res]
        result = db.insert_one(
            {
                "user_id": user_id,
                "model_id": model_id,
                "req": req,
                "res": res,
                "created": datetime.datetime.now(),
            }
        )
    except Exception as e:
        print("Error logging to db:", e)
        return None
    return result.inserted_id


def log_to_db_modelhub(
    db: Collection,
    auth: AuthParams,
    params: ChatParams,
    response,
):
    """Save a message to the database"""
    try:
        result = db.insert_one(
            {
                "message_id": str(uuid.uuid4()),
                "user_id": auth.user_name,
                "model": params.model,
                "prompt": params.prompt,
                "stream": params.stream,
                "parameters": params.parameters,
                "response": response.dict(),
                "created_time": datetime.datetime.now(),
            }
        )
    except Exception as e:
        print(f"Failed to save message: {e}")
        return None
    return result.inserted_id


def make_completion(res, model):
    return ChatCompletion(
        id=uuid.uuid4().hex,
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(role="assistant", content=res),
            )
        ],
        object="chat.completion",
        created=int(time.time()),
        model=model,
    )


def make_chunk(res_delta, model):
    return ChatCompletionChunk(
        id=uuid.uuid4().hex,
        choices=[
            ChunkChoice(
                delta=ChoiceDelta(
                    content=res_delta,
                    role="assistant",
                ),
                finish_reason=None,
                index=0,
            )
        ],
        object="chat.completion.chunk",
        created=int(time.time()),
        model=model,
    )


def hash_password(password: str):
    """
    Hash a password"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
