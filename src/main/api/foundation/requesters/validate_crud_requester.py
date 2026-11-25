# будет возвращать python объёкт будет распоковывать ответ в модель и возвращать нам это в тест
from enum import Enum
from typing import Optional
import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec

        )

    def post(self, model: Optional[BaseModel]) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def get(self, account_id: int) -> Optional[BaseModel]:
        response = self.crud_requester.get(account_id)

        with allure.step(
                f"GET {Config.fetch('backendUrl')}"
                f"{self.endpoint.value.url}/{account_id} and Validated Model"):
            allure.attach(
                f"Validated Model response: "
                f"{self.endpoint.value.response_model.__name__}"
            )

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


