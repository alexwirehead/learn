from requests import request, Response
from requests.auth import HTTPBasicAuth

from lib import (
    RABBIT_ROOT_API_URL,
    RABBIT_USERNAME,
    RABBIT_PASSWORD,
    mod_logger)

logger = mod_logger()


class HttpClient:
    def __init__(self):
        self.__root_api_url = RABBIT_ROOT_API_URL
        self.__basic_auth_token = HTTPBasicAuth(RABBIT_USERNAME, RABBIT_PASSWORD)

    def call_api(self, method: str, api_playload: dict, api_uri: str) -> Response:
        url = self.__root_api_url + api_uri
        resp = request(method=method, url=url, json=api_playload, auth=self.__basic_auth_token)
        return resp
