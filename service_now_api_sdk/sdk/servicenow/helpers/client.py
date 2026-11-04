import json
from functools import wraps

import requests

from service_now_api_sdk.settings import (
    SERVICENOW_API_PASSWORD,
    SERVICENOW_API_TOKEN,
    SERVICENOW_API_USER,
    SERVICENOW_URL,
)





class Client:
    base_url = SERVICENOW_URL
    default_path = ""

    def __init__(self, host_url: str=None, user: str=None, password: str=None, api_token: str=None):
        self.base_url = host_url or SERVICENOW_URL
        self.api_token = api_token or SERVICENOW_API_TOKEN
        self.user = user or SERVICENOW_API_USER
        self.password = password or SERVICENOW_API_PASSWORD
    
    def headers_replace(self, default_headers: dict = None):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_token:
            headers["Authorization"] = (f"Bearer {self.api_token}",)
        if default_headers:
            headers = {**headers, **default_headers}
        default_headers = headers

    def __http_request(
        self,
        method: str,
        path: str,
        headers: dict = None,
        data=None,
        params: dict = None,
        timeout: int = None
    ):
        if data is None:
            data = {}

        if params is None:
            params = {}

        if self.api_token:
            return requests.request(
                method=method,
                url=f"{self.base_url}/{path}",
                headers=headers,
                data=json.dumps(data),
                params=params,
                timeout=timeout
            )

        if self.user and self.password:
            return requests.request(
                method=method,
                url=f"{self.base_url}/{path}",
                headers=headers,
                data=json.dumps(data),
                params=params,
                auth=(self.user, self.password),
                timeout=timeout
            )

    def post(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None, timeout: int = None
    ):
        return self.__http_request(
            method="POST", path=path, headers=headers, data=data, params=params, timeout=timeout
        )

    def get(self, path: str, headers: dict = None, params: dict = None, timeout: int = None):
        return self.__http_request(
            method="GET", path=path, headers=headers, params=params, timeout=timeout
        )

    def put(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None, timeout: int = None
    ):
        return self.__http_request(
            method="PUT", path=path, headers=headers, data=data, params=params, timeout=timeout
        )

    def patch(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None, timeout: int = None
    ):
        return self.__http_request(
            method="PATCH", path=path, headers=headers, data=data, params=params, timeout=timeout
        )

    def delete(self, path: str, headers: dict = None, data: dict = None, timeout: int = None):
        return self.__http_request(
            method="DELETE", path=path, headers=headers, data=data, timeout=timeout
        )
