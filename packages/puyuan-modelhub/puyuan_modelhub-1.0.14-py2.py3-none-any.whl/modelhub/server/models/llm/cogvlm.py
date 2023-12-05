from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from modelhub.server.models.base import BaseChatModel
from typing import Optional, Dict, List, Any
import requests


class CogVLMModel(BaseChatModel):
    host: str
    port: int
    model: str = "cogvlm"
    max_tokens: int = 1650
    temperature: float = 0.3

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        image_path = parameters["image_path"]
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/chat",
                params={"query": prompt, "image_path": image_path},
            ).json()
            return TextGenerationOutput(
                generated_text=response["response"],
            )
        except Exception as e:
            return TextGenerationOutput(
                generated_text=f"Error: {e}",
            )
