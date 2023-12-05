from modelhub.common.types import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from modelhub.server.models.base import BaseChatModel
from typing import Optional, Dict, List, Any
import hashlib
import base64
import hmac
import uuid
import requests
import json
from datetime import datetime, timedelta


class CPMModel(BaseChatModel):
    app_id: str
    app_key: str
    temperature: float = 0.3

    @staticmethod
    def get_md5_base64(s: str) -> str:
        if str is None:
            return None
        md5 = hashlib.md5(s.encode("utf-8")).digest()
        return base64.b64encode(md5).decode("utf-8")

    @staticmethod
    def get_signature_base64(data: str, key: str) -> str:
        key_bytes = key.encode("utf-8")
        data_bytes = data.encode("utf-8")
        hmac_obj = hmac.new(key_bytes, data_bytes, hashlib.sha256)
        return base64.b64encode(hmac_obj.digest()).decode("utf-8")

    @staticmethod
    def get_response(
        msg: str, app_id: str, app_key: str, params: Dict[str, Any], msg_only=True
    ) -> str:
        try:
            url_queries = None
            body_data = {
                "model": "cpm-c-80",
                "actionType": "conv",
                "message": [{"role": "USER", "content": msg}],
                "maxLength": 4096,
                "modelParam": {
                    "repetitionPenalty": 1.02,
                    "ngramPenalty": 1.02,
                    "temperature": 1.02,
                    **params,
                },
            }
            content_md5 = CPMModel.get_md5_base64(json.dumps(body_data))
            method = "POST"
            accept = "*/*"
            content_type = "application/json"
            timestamp = int((datetime.utcnow() + timedelta(hours=8)).timestamp() * 1000)
            mode = "Signature"
            nonce = str(uuid.uuid4())
            sbuffer = "\n".join(
                [
                    method,
                    accept,
                    content_type,
                    str(timestamp),
                    content_md5,
                    mode,
                    nonce,
                    url_queries if url_queries else "",
                ]
            )
            signature = CPMModel.get_signature_base64(sbuffer, app_key)
            headers = {
                "Content-Type": content_type,
                "Accept": accept,
                "X-Model-Best-Open-Ca-Time": str(timestamp),
                "Content-MD5": content_md5,
                "X-Model-Best-Open-App-Id": app_id,
                "X-Model-Best-Open-Ca-Mode": mode,
                "X-Model-Best-Open-Ca-Nonce": nonce,
                "X-Model-Best-Open-Ca-Signature": signature,
            }
            api_url = "https://api.modelbest.cn/openapi/v1/conversation"
            response = requests.post(api_url, headers=headers, json=body_data)
            # print("result:", response.text)
            d = json.loads(response.text)
            if msg_only:
                return d["data"]["message"]["content"]
            return d
        except Exception as e:
            # TODO: log error
            raise e

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
        }

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters = {**self.default_parameters, **parameters}
        response = CPMModel.get_response(
            prompt, self.app_id, self.app_key, parameters, msg_only=False
        )
        if response["code"] != 0:
            raise Exception(response["message"])
        return TextGenerationOutput(
            generated_text=response["data"]["message"]["content"],
            details=TextGenerationStreamDetails(
                finish_reason=response["data"]["stopReason"],
                prompt_tokens=0,
                generated_tokens=response["data"]["totalTokens"],
            ),
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        raise NotImplementedError("streaming is not supported for CPM")
