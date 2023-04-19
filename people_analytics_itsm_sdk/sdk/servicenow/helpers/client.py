import json
from functools import wraps

import requests

from people_analytics_itsm_sdk.settings import (
    ITSM_SERVICENOW_API_PASSWORD,
    ITSM_SERVICENOW_API_TOKEN,
    ITSM_SERVICENOW_API_USER,
    ITSM_SERVICENOW_URL,
)


def headers_replace(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if ITSM_SERVICENOW_API_TOKEN:
            headers["Authorization"] = (f"Bearer {ITSM_SERVICENOW_API_TOKEN}",)

        if kwargs.get("headers"):
            headers = {**headers, **kwargs.get["headers"]}

        kwargs["headers"] = headers

        return f(*args, **kwargs)

    return decorated_function


class Client:
    base_url = ITSM_SERVICENOW_URL
    default_path = ""

    @headers_replace
    def __http_request(
        self,
        method: str,
        path: str,
        headers: dict = None,
        data=None,
        params: dict = None,
    ):
        if data is None:
            data = {}

        if params is None:
            params = {}

        if ITSM_SERVICENOW_API_TOKEN:
            return requests.request(
                method=method,
                url=f"{self.base_url}/{path}",
                headers=headers,
                data=json.dumps(data),
                params=params,
            )

        if ITSM_SERVICENOW_API_USER and ITSM_SERVICENOW_API_PASSWORD:
            return requests.request(
                method=method,
                url=f"{self.base_url}/{path}",
                headers=headers,
                data=json.dumps(data),
                params=params,
                auth=(ITSM_SERVICENOW_API_USER, ITSM_SERVICENOW_API_PASSWORD),
            )

    def post(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None
    ):
        return self.__http_request(
            method="POST", path=path, headers=headers, data=data, params=params
        )

    def get(self, path: str, headers: dict = None, params: dict = None):
        return self.__http_request(
            method="GET", path=path, headers=headers, params=params
        )

    def put(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None
    ):
        return self.__http_request(
            method="PUT", path=path, headers=headers, data=data, params=params
        )

    def patch(
        self, path: str, headers: dict = None, data: dict = None, params: dict = None
    ):
        return self.__http_request(
            method="PATCH", path=path, headers=headers, data=data, params=params
        )

    def delete(self, path: str, headers: dict = None, data: dict = None):
        return self.__http_request(
            method="DELETE", path=path, headers=headers, data=data
        )
