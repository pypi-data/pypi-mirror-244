from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from modelhub.common.types import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    EmbeddingOutput,
)
from modelhub.server.models.base import BaseChatModel
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, root_validator, PrivateAttr
import requests
import modelhub.server.utils as utils
import json


class _MinimaxEndpointClient(BaseModel):
    group_id: str
    api_key: str
    api_url: str
    host: str

    @root_validator(pre=True, allow_reuse=True)
    def set_api_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "api_url" not in values:
            host = values["host"]
            group_id = values["group_id"]
            api_url = f"{host}/v1/text/chatcompletion?GroupId={group_id}"
            values["api_url"] = api_url
        return values

    def stream(self, request: Any) -> Any:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        request["use_standard_sse"] = True
        request["stream"] = True
        response = requests.post(
            self.api_url,
            headers=headers,
            json=request,
            stream=True,
        )
        # TODO: error handling and automatic retries
        for chunk in response.iter_lines(decode_unicode=True, delimiter="\n\n"):
            try:
                chunk = json.loads(chunk[5:])
                yield chunk
            except:
                pass

    def post(self, request: Any) -> Any:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.api_url, headers=headers, json=request)
        # TODO: error handling and automatic retries
        if not response.ok:
            raise ValueError(f"HTTP {response.status_code} error: {response.text}")
        if response.json()["base_resp"]["status_code"] > 0:
            raise ValueError(
                f"API {response.json()['base_resp']['status_code']}"
                f" error: {response.json()['base_resp']['status_msg']}"
            )
        return response.json()["reply"]

    def get_embeddings(self, request: Any) -> Any:
        embedding_api_url = (
            f"https://api.minimax.chat/v1/embeddings?GroupId={self.group_id}"
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        request["model"] = "embo-01"  # max tokens is 4096
        request["type"] = request.get("type", "query")
        assert request["type"] in ["db", "query"]

        response = requests.post(embedding_api_url, headers=headers, json=request)
        if not response.ok:
            raise ValueError(f"HTTP {response.status_code} error: {response.text}")
        if response.json()["base_resp"]["status_code"] > 0:
            raise ValueError(
                f"API {response.json()['base_resp']['status_code']}"
                f" error: {response.json()['base_resp']['status_msg']}"
            )
        return response.json()["vectors"]


class Minimax(BaseChatModel):
    """
    Minimax chat model
    documentation: https://api.minimax.chat/document
    """

    _client: _MinimaxEndpointClient = PrivateAttr()
    minimax_api_key: str
    minimax_group_id: str
    model: str = "abab5.5-chat"
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.95

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = _MinimaxEndpointClient(
            host="https://api.minimax.chat",
            api_key=self.minimax_api_key,
            group_id=self.minimax_group_id,
        )

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "tokens_to_generate": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        def convert_openai_to_minimax(
            messages: List[Dict[str, str]]
        ) -> List[Dict[str, str]]:
            mx_msgs = []
            for message in messages:
                if message["role"] == "user":
                    mx_msgs.append({"sender_type": "USER", "text": message["content"]})
                else:
                    mx_msgs.append({"sender_type": "BOT", "text": message["content"]})
            return mx_msgs

        messages = convert_openai_to_minimax(req["messages"])
        parameters = {
            "model": self.model,
            "tokens_to_generate": req.get("max_tokens", self.max_tokens),
            "temperature": req.get("temperature", self.temperature),
            "top_p": req.get("top_p", self.top_p),
        }

        stream = req.pop("stream", False)
        request = {"messages": messages, **parameters}

        def chat():
            response = self._client.post(request)
            return utils.make_completion(response, self.model)

        def stream_chat():
            for chunk in self._client.stream(request):
                if len(chunk["choices"]) == 0:
                    continue
                yield utils.make_chunk(chunk["choices"][0]["delta"], self.model)

        return stream_chat() if stream else chat()

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        request = {
            "messages": [{"sender_type": "USER", "text": prompt}],
            **self.default_params,
            **parameters,
        }
        return TextGenerationOutput(generated_text=self._client.post(request))

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        requests = {
            "messages": [{"sender_type": "USER", "text": prompt}],
            **self.default_params,
            **parameters,
        }
        generated_text = ""
        for chunk in self._client.stream(requests):
            if len(chunk["choices"]) == 0:
                continue
            delta = chunk["choices"][0]["delta"]

            generated_text += delta
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(
                    id=0,
                    text=delta,
                    logprob=0,
                    special=False,
                )
            )
        yield TextGenerationStreamOutput(
            token=TextGenerationStreamToken(id=0, text="", logprob=0, special=False),
            generated_text=generated_text,
        )

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        prompt = [prompt] if isinstance(prompt, str) else prompt
        requests = {
            "texts": prompt,
            **parameters,
        }
        return EmbeddingOutput(embeddings=self._client.get_embeddings(requests))
