from pydantic import BaseModel
from typing import Dict, Any, List


class AuthParams(BaseModel):
    """AuthParams: Parameters for authentication"""

    user_name: str
    user_password: str


class ChatParams(BaseModel):
    """ChatParams: Parameters for chat"""

    prompt: str
    model: str
    stream: bool = False
    parameters: Dict[str, Any] = {}


class TokensParams(BaseModel):
    """TokensParams: Parameters for tokens"""

    prompt: str
    model: str
    parameters: Dict[str, Any] = {}


class EmbeddingParams(BaseModel):
    """EmbeddingParams: Parameters for embedding"""

    prompt: str | List[str]
    model: str
    parameters: Dict[str, Any] = {}
