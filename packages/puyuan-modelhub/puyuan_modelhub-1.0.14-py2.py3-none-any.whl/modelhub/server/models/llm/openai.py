from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from modelhub.server.models.base import BaseChatModel
from typing import Optional, Dict, List, Any, Generator, Literal
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel
import tiktoken


class ChatOpenAI(BaseChatModel, arbitrary_types_allowed=True):
    api_key: str
    api_type: Literal["open_ai", "azure"] = "open_ai"
    azure_endpoint: Optional[str] = None
    api_version: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.3
    client: OpenAI = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.api_type == "azure":
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.azure_endpoint,
                api_version=self.api_version,
            )
        else:
            self.client = OpenAI(
                api_key=self.api_key,
            )

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "temperature": self.temperature,
        }

    def n_tokens(self, prompt: str, parameters: Dict[str, Any]) -> int:
        model = "gpt-3.5-turbo" if self.api_type == "azure" else self.model
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(prompt, **parameters))

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        req["model"] = self.model
        return self.client.chat.completions.create(**req)

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters = {**self.default_parameters, **parameters}
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        chat_completion = self.client.chat.completions.create(
            messages=messages, **parameters
        )
        return TextGenerationOutput(
            generated_text=chat_completion.choices[0].message.content,
            details=TextGenerationStreamDetails(
                finish_reason=chat_completion.choices[0].finish_reason,
                prompt_tokens=chat_completion.usage.prompt_tokens,
                generated_tokens=chat_completion.usage.completion_tokens,
            ),
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        parameters = {**self.default_parameters, **parameters}
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **parameters,
        )

        generated_text = ""
        for delta in response:
            if len(delta.choices) == 0:
                continue
            if delta.choices[0].finish_reason == "stop":
                yield TextGenerationStreamOutput(
                    token=TextGenerationStreamToken(
                        id=0,
                        text="",
                        logprob=0,
                        special=False,
                    ),
                    generated_text=generated_text,
                )
            else:
                delta_content = delta.choices[0].delta.content or ""
                generated_text += delta_content
                yield TextGenerationStreamOutput(
                    token=TextGenerationStreamToken(
                        id=0,
                        text=delta_content,
                        logprob=0,
                        special=False,
                    )
                )

    async def astream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        raise NotImplementedError

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        embed_out = self.client.embeddings.create(
            input=prompt, model=self.model, **parameters
        )
        return EmbeddingOutput(embeddings=[x.embedding for x in embed_out.data])
