from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from openai.types.chat.chat_completion import Choice, ChatCompletionMessage
from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
    TextGenerationDetails,
    BaseMessage,
    AIMessage,
    UserMessage,
    ToolMessage,
)
from modelhub.server.models.errors import *
from modelhub.server.models.base import BaseChatModel
from typing import Generator, Optional, Dict, List, Any
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
import json
import uuid
import time
import os
import modelhub.server.utils as utils


def torch_gc(device: int = 0):
    if torch.cuda.is_available():
        with torch.cuda.device(device):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


def gpu_env(device: int | str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if isinstance(device, str):
                os.environ["CUDA_VISIBLE_DEVICES"] = device
            res = func(*args, **kwargs)
            if isinstance(device, str):
                os.environ["CUDA_VISIBLE_DEVICES"] = ""
            return res

        return wrapper

    return decorator


class SentenceTransformerModel(BaseChatModel):
    local_model_path: str
    cuda_device: int = 0
    model: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.model = SentenceTransformer(self.local_model_path)
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Embedding Model: {e}")

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        prompt = [prompt] if isinstance(prompt, str) else prompt
        try:
            embeddings = self.model.encode(prompt)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate embeddings: {e}")
        return EmbeddingOutput(embeddings=embeddings.tolist())


class YiBaseModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading deepseek model")
            # os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                use_flash_attention_2=True,
                torch_dtype=torch.bfloat16,
            ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            # os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Deepseek Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=256,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters.pop("history")
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(inputs.input_ids, **parameters)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )


class DeepseekBaseModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading deepseek model")
            # os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                use_flash_attention_2=True,
                torch_dtype=torch.bfloat16,
            ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            # os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Deepseek Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=128,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters.pop("history")
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(**inputs, **parameters)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )


class DeepseekModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading deepseek model")
            # os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                use_flash_attention_2=True,
                torch_dtype=torch.bfloat16,
            ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            # os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Deepseek Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=512,
            do_sample=False,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1,
            eos_token_id=32021,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        try:
            inputs = self.tokenizer.apply_chat_template(
                messages, return_tensors="pt"
            ).to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(inputs, **parameters)
            response = self.tokenizer.decode(
                outputs[0][len(inputs[0]) :], skip_special_tokens=True
            )
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        if isinstance(response, dict):
            response = json.dumps(response, ensure_ascii=False)
        return TextGenerationOutput(
            generated_text=response,
            history=messages + [{"role": "assistant", "content": response}],
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )


class ChatGLMLocal(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    temperature: float = 0.01
    top_p: float = 0.9
    is_multi_gpu: bool = False
    cuda_device: int | str = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def count_tokens(self, prompt: str, **kwargs) -> int:
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
        return len(self.tokenizer(prompt)["input_ids"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            if isinstance(self.cuda_device, str):
                self.is_multi_gpu = True
            print(f"Loading chatglm model from {self.local_model_path}")
            if self.is_multi_gpu:
                os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
                print(self.cuda_device)
                self.model = AutoModel.from_pretrained(
                    self.local_model_path, trust_remote_code=True, device_map="auto"
                )
            else:
                self.model = AutoModel.from_pretrained(
                    self.local_model_path, trust_remote_code=True
                ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            self.model.eval()
            print("Model loaded")
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
        except Exception as e:
            print(f"Failed to load chatglm model {e}")
            raise ModelLoadError(f"Failed to load ChatGLM Model: {e}")

    def n_tokens(self, prompt: str, parameters: Dict[str, Any]) -> int:
        encoding = self.tokenizer.encode(prompt, **parameters)
        return len(encoding)

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        @gpu_env(self.cuda_device)
        def chat():
            res, history = self.model.chat(
                self.tokenizer,
                req["messages"][-1]["content"],
                history=req["messages"][:-1],
                temperature=req.get("temperature", self.temperature),
                top_p=req.get("top_p", self.top_p),
            )
            return utils.make_completion(res, req["model"])

        @gpu_env(self.cuda_device)
        def stream_chat():
            response = ""
            for res_delta, history in self.model.stream_chat(
                self.tokenizer,
                req["messages"][-1]["content"],
                history=req["messages"][:-1],
                temperature=req.get("temperature", self.temperature),
                top_p=req.get("top_p", self.top_p),
            ):
                yield utils.make_chunk(res_delta[len(response) :], req["model"])
                response = res_delta

        stream = req.get("stream", False)
        if stream:
            return stream_chat()
        else:
            return chat()

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        if self.is_multi_gpu:
            os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
        tokens_count = self.count_tokens(prompt)
        max_length = parameters.get("max_length", 8192)
        if tokens_count > max_length:
            raise ModelGenerateError(
                f"Input length {tokens_count} exceeds maximum length {max_length}"
            )
        try:
            response, history = self.model.chat(self.tokenizer, prompt, **parameters)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            if self.is_multi_gpu:
                os.environ["CUDA_VISIBLE_DEVICES"] = ""
            if not self.is_multi_gpu:
                torch_gc(self.cuda_device)
        if isinstance(response, dict):
            response = json.dumps(response, ensure_ascii=False)
        return TextGenerationOutput(
            generated_text=response,
            history=history,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        if self.is_multi_gpu:
            os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
        tokens_count = self.count_tokens(prompt)
        max_length = parameters.get("max_length", 8192)
        if tokens_count > max_length:
            raise ModelGenerateError(
                f"Input length {tokens_count} exceeds maximum length {max_length}"
            )
        try:
            response = ""
            for res_delta, history in self.model.stream_chat(
                self.tokenizer, prompt, **parameters
            ):
                yield TextGenerationStreamOutput(
                    token=TextGenerationStreamToken(
                        id=0,
                        text=res_delta[len(response) :],
                        logprob=0,
                        special=False,
                    ),
                    history=[],
                    generated_text=None,
                )
                response = res_delta
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(
                    id=0,
                    text="",
                    logprob=0,
                    special=False,
                ),
                history=history,
                generated_text=response,
            )
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            if self.is_multi_gpu:
                os.environ["CUDA_VISIBLE_DEVICES"] = ""
            if not self.is_multi_gpu:
                torch_gc(self.cuda_device)
