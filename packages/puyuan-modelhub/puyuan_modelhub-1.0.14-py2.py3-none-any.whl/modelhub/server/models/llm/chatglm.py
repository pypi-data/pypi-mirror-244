from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
import time
from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from modelhub.server.models.base import BaseChatModel
from typing import Optional, Dict, List, Any
import zhipuai
import modelhub.server.utils as utils
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice, ChoiceDelta


class ChatGLMModel(BaseChatModel):
    api_key: str
    model: str = "chatglm_pro"
    temperature: float = 0.01

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        zhipuai.api_key = self.api_key

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
        }

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        parameters = {
            "temperature": req.get("temperature", self.temperature),
        }
        stream = req.pop("stream", False)

        def stream_chat():
            response = zhipuai.model_api.sse_invoke(
                model=self.model, prompt=req["messages"], **parameters
            )
            generated_text = ""
            for event in response.events():
                if event.event == "add":
                    generated_text += event.data
                    yield utils.make_chunk(event.data, self.model)

        def chat():
            res = zhipuai.model_api.invoke(
                model=self.model, prompt=req["messages"], **parameters
            )
            if res["code"] != 200:
                return utils.make_completion(res["msg"], self.model)
            return ChatCompletion(
                id=res["data"]["request_id"],
                choices=[
                    Choice(
                        finish_reason="stop", index=0, message=res["data"]["choices"][0]
                    )
                ],
                object="chat.completion",
                created=int(time.time()),
                model=self.model,
                usage=res["data"]["usage"],
            )

        return stream_chat() if stream else chat()

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters = {**self.default_parameters, **parameters}
        response = zhipuai.model_api.invoke(
            model=self.model, prompt=prompt, **parameters
        )
        if response["code"] == 200:
            return TextGenerationOutput(
                generated_text=response["data"]["choices"][0]["content"],
                details=TextGenerationStreamDetails(
                    finish_reason=response["msg"],
                    prompt_tokens=response["data"]["usage"]["prompt_tokens"],
                    generated_tokens=response["data"]["usage"]["completion_tokens"],
                ),
            )
        else:
            return TextGenerationOutput(
                generated_text=f"Failed to generate text: {response}",
                details=TextGenerationStreamDetails(
                    finish_reason=response["msg"],
                ),
            )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        message_dicts = [{"role": "user", "content": prompt}]
        parameters.pop("history")
        parameters = {**self.default_parameters, **parameters}
        response = zhipuai.model_api.sse_invoke(
            model=self.model, prompt=message_dicts, **parameters
        )
        generated_text = ""
        for event in response.events():
            if event.event == "add":
                generated_text += event.data
                yield TextGenerationStreamOutput(
                    token=TextGenerationStreamToken(
                        id=0, text=event.data, logprob=0, special=False
                    ),
                )
        yield TextGenerationStreamOutput(
            token=TextGenerationStreamToken(id=0, text="", logprob=0, special=False),
            generated_text=generated_text,
        )

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        strs = [prompt] if isinstance(prompt, str) else prompt
        embedding_model = "text_embedding"
        embeddings = []
        for s in strs:
            response = zhipuai.model_api.invoke(
                model=embedding_model, prompt=prompt, **parameters
            )
            if response["code"] == 200:
                embeddings.append(response["data"]["embedding"])
            else:
                raise Exception(f"Failed to generate embeddings: {response}")
        return EmbeddingOutput(embeddings=embeddings)
