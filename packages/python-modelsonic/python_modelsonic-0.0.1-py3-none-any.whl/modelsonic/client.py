from __future__ import annotations

import logging
import json
import httpx
from typing import Any, Dict, List

from modelsonic.enums import ModelSonicModelsEnum

logger = logging.getLogger(__name__)


class ModelSonicClient:
    models = None
    request_timeout = 60

    def __init__(self, base_url, api_key, request_timeout: int = 60):
        self.base_url = base_url
        self.api_key = api_key
        self.request_timeout = request_timeout

    async def _async_api_call(self, *, path: str, method: str, payload: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method,
                    url=self.base_url + "/api" + path,
                    headers={
                        "content-type": "application/json",
                        "ws-secret": self.api_key,
                    },
                    json=payload,
                    timeout=self.request_timeout,
                )
                if response.status_code == 200:
                    return response.json()
                # this needs to be handled specifically as parsing null response throws error
                elif (
                    response.status_code == 202
                    or response.status_code == 204
                ):
                    return None
                else:
                    raise Exception(response.json())
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise TimeoutError("Request timed out")
        
    def _api_call(self, *, path: str, method: str, payload: dict):
        try:
            with httpx.Client() as client:
                response = client.request(
                    method,
                    url=self.base_url + "/api" + path,
                    headers={
                        "content-type": "application/json",
                        "ws-secret": self.api_key,
                    },
                    json=payload,
                    timeout=self.request_timeout,
                )
                if response.status_code == 200:
                    return response.json()
                # this needs to be handled specifically as parsing null response throws error
                elif (
                    response.status_code == 202
                    or response.status_code == 204
                ):
                    return None
                else:
                    raise Exception(response.json())
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise TimeoutError("Request timed out")

    async def astream_events(self, *, path: str, method: str, payload: dict):
        """
        Async Stream events from the model router.
        """
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    method,
                    url=f"{self.base_url}/api{path}",
                    data=json.dumps(payload),
                    headers={"Content-type": "application/json", "ws-secret": self.api_key},
                    timeout=self.request_timeout,
                ) as response:
                    async for line in response.aiter_lines():
                        try:
                            if line.strip() == "":
                                continue

                            line_type, line_data = (
                                segment.strip() for segment in line.split(":", 1)
                            )

                            if line_type != "data":
                                continue

                            data: dict = json.loads(line_data.strip())

                            yield data
                        except Exception:
                            continue
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise TimeoutError("Request timed out")

    def stream_events(self, *, path: str, method: str, payload: dict):
        """
        Stream events from the model router.
        """
        try:
            with httpx.Client() as client:
                with client.stream(
                    method=method,
                    url=f"{self.base_url}/api{path}",
                    data=json.dumps(payload),
                    headers={"Content-type": "application/json", "ws-secret": self.api_key},
                    timeout=self.request_timeout,
                ) as response:
                    for line in response.iter_lines():
                        try:
                            if line.strip() == "":
                                continue

                            line_type, line_data = (
                                segment.strip() for segment in line.split(":", 1)
                            )

                            if line_type != "data":
                                continue

                            data = json.loads(line_data.strip())

                            yield data
                        except Exception:
                            continue
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise TimeoutError("Request timed out")
    
    def get_all_models(self):
        """Get all available models from Writesonic Model Router"""
        response = self._api_call(path="/v1/model/all", method="GET", payload={})
        self.models = response
        return self.models

    def get_model_by_name(self, model_name: str):
        if self.models is None:
            self.models = self.get_all_models()

        model = next(
            (model for model in self.models if model["name"] == model_name), None
        )
        if model is None:
            raise Exception(f"Model {model_name} not found")
        return model

    def generate(self, *, params_list: Dict[str, Any]):
        return self._api_call(
            path="/v1/generate",
            method="POST",
            payload={
                "stream": False,
                "data": params_list,
            },
        )
    
    async def agenerate(self, *, params_list: Dict[str, Any]):
        return await self._async_api_call(
            path="/v1/generate",
            method="POST",
            payload={
                "stream": False,
                "data": params_list,
            },
        )

    def generate_stream(self, *, params_list: Dict[str, Any]):
        return self.stream_events(
            path="/v1/generate",
            method="POST",
            payload={
                "stream": True,
                "data": params_list,
            },
        )

    async def agenerate_stream(self, *, params_list: Dict[str, Any]):
        return self.astream_events(
            path="/v1/generate",
            method="POST",
            payload={
                "stream": True,
                "data": params_list,
            },
        )

    @classmethod
    def convert_message_to_text(
        cls,
        role: str,
        content: str,
        human_prompt: str = "\n\nHuman:",
        ai_prompt: str = "\n\nAssistant:",
    ) -> str:
        if role == "user":
            message_text = f"{human_prompt} {content}"
        elif role == "assistant":
            message_text = f"{ai_prompt} {content}"
        elif role == "system":
            message_text = content
        else:
            raise ValueError(f"Got unknown type {role}")
        return message_text

    @classmethod
    def convert_messages_to_anthropic_prompt(cls, messages: List[Dict]) -> str:
        text = "".join(
            cls.convert_message_to_text(message["role"], message["content"])
            for message in messages
        )
        # trim off the trailing ' ' that might come from the "Assistant: "
        text = text.rstrip()
        # check if text does not end with "\n\nAssistant:"
        if not text.endswith("\n\nAssistant:"):
            text += "\n\nAssistant:"

        return text

    def extract_prompt_params(self, params: Dict) -> Dict:
        prompt_params_keys = [
            "messages",
            "max_tokens",
            "temperature",
            "top_p",
            "n",
            "user",
            "prompt",
            "frequency_penalty",
            "presence_penalty",
            "functions",
            "function_call",
        ]
        modified_params = {
            key: params.get(key) for key in prompt_params_keys if key in params
        }
        if params["model"] in [ModelSonicModelsEnum.CLAUDE_INSTANT_12.value]:
            modified_params["prompt"] = self.convert_messages_to_anthropic_prompt(
                modified_params["messages"]
            )
            del modified_params["messages"]
            # TODO: remove this once we have a better way to handle this
            if "max_tokens" not in modified_params:
                modified_params["max_tokens"] = 1000
        return modified_params
    
    def create_params_list(
        self,
        params_list: Dict,
    ) -> List[Dict]:
        modified_params_list = []
        for index, params in enumerate(params_list):
            if "model" not in params:
                raise Exception("Model name is required")
            model = self.get_model_by_name(params["model"])
            modified_params_list.append(
                {
                    "order": index + 1,
                    "modelId": model["id"],
                    "providerId": model["providerId"],
                    "promptParams": self.extract_prompt_params(params),
                }
            )
        return modified_params_list

    def generate_with_params_list(
        self,
        *,
        params_list: Dict[str, Any],
        is_stream: bool = False,
    ):
        """
        model is provided in the params_list
        """
        modified_params_list = self.create_params_list(params_list)
        if is_stream:
            return self.generate_stream(params_list=modified_params_list)
        return self.generate(params_list=modified_params_list)

    async def agenerate_with_params_list(
        self,
        *,
        params_list: Dict[str, Any],
        is_stream: bool = False,
    ):
        """
        model is provided in the params_list
        """
        modified_params_list = self.create_params_list(params_list)
        if is_stream:
            return await self.agenerate_stream(params_list=modified_params_list)
        return await self.agenerate(params_list=modified_params_list)
