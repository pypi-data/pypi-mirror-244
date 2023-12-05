from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, List, Generator
from modelhub.common.types import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    EmbeddingOutput,
)
from openai.types.chat import (
    ChatCompletion,
    CompletionCreateParams,
    ChatCompletionChunk,
)
from openai._streaming import Stream
from openai.types.embedding import Embedding
from openai.types.embedding_create_params import EmbeddingCreateParams


class BaseChatModel(BaseModel, ABC):
    """
    BaseChatModel: Base class for chat models
    """

    # @abstractmethod
    async def achat(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationOutput:
        """Chat with a model asynchronously"""
        raise NotImplementedError("achat is not supported for this model")

    # @abstractmethod
    async def astream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        """Stream chat with a model asynchronously"""
        raise NotImplementedError("astream is not supported for this model")

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """Chat with a model"""
        raise NotImplementedError("chat is not supported for this model")

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        """Chat with a model"""
        raise NotImplementedError("chat is not supported for this model")

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        """Stream chat with a model"""
        raise NotImplementedError("streaming is not supported for this model")

    def n_tokens(self, prompt: str, parameters: Dict[str, Any]) -> int:
        """Get the number of tokens in a prompt"""
        raise NotImplementedError("n_tokens is not supported for this model")

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        """Get embeddings from a model"""
        raise NotImplementedError("Embeddings are not supported for this model")

    def get_embeddings_openai(self, params: EmbeddingCreateParams) -> Embedding:
        """Get embeddings from a model"""
        raise NotImplementedError("Embeddings are not supported for this model")
