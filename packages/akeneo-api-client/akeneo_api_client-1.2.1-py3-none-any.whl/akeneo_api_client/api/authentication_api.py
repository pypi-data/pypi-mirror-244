import base64

from .request.dict_serialize import DictSerialize
from .request.json_serializable import JsonSerializable


class AuthenticationApi:

    TOKEN_URI = "api/oauth/v1/token"

    def __init__(self, http_client, uri_generator):
        self.http_client = http_client
        self.uri_generator = uri_generator

    def authenticate_by_password(self, username: str, password: str, client_id: str, secret: str):
        body = {
            "grant_type": "password",
            "username": username,
            "password": password
        }

        return self.authenticate(client_id, secret, DictSerialize(body))

    def authenticate_by_refresh_token(self, client_id: str, secret: str, refresh_token: str):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        return self.authenticate(client_id, secret, DictSerialize(body))

    def authenticate(self, client_id: str, secret: str, body: JsonSerializable):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode((client_id + ":" + secret).encode('utf-8')).decode('utf-8')
        }

        uri = self.uri_generator.generate(self.TOKEN_URI)

        response = self.http_client.send_request("POST", uri, headers, body)
        return response.json()
