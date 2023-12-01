import requests
from requests.models import Response

from .akeneo_api_error import AkeneoApiError
from akeneo_api_client.api.request.json_serializable import JsonSerializable


class HttpClient:

    def send_request(self, method: str, uri: str, headers: dict, body: JsonSerializable = None) -> Response:
        data = None
        if body is not None:
            data = body.serialize()

        response = requests.request(method, uri, headers=headers, data=data)
        if response.status_code >= 400:
            raise AkeneoApiError(response)

        return response
