import modelhub.server.models as g_models
from modelhub.server.models.errors import *
from typing import List
from pydantic import BaseModel, Field
from typing import Optional
import time


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


class ModelImpl(BaseModel):
    model_class: str
    model_kwargs: dict = {}
    chat_kwargs: Optional[dict] = None


def validate_models(config: dict) -> List[ModelImpl]:
    _models = {}
    for id, cfg in config.items():
        model = ModelImpl(**cfg)
        if not hasattr(g_models, model.model_class):
            raise ModelNotFoundError(f"model {model.model_class} not found in models")
        _models[id] = model
    return _models


class ModelProvider(object):
    def __init__(self, config={}) -> None:
        """提供各种模型，包括embedding的模型和llm的模型"""
        self._models = validate_models(config)
        self._cache = {}
        self._model_list = ModelList(
            data=[ModelCard(id=model_name) for model_name in self._models.keys()]
        )

    @property
    def models(self):
        return list(self._models.keys())

    def list_models(self):
        return self._model_list

    def get_supported_params(self, model_name: str):
        return {"chat": [], "embedding": []}

    def provide(self, id: str, kwargs: dict = {}):
        if id in self._cache:
            return self._cache[id]
        if not id in self._models:
            raise ModelNotFoundError(f"model {id} not found")
        kwargs = kwargs or self._models[id].model_kwargs
        self._cache[id] = getattr(g_models, self._models[id].model_class)(**kwargs)
        return self._cache[id]
