from requests.models import Response

from akeneo_api_client.api.request.json_serializable import JsonSerializable


class ResourceClient:

    def __init__(self, uri_generator, authenticated_http_client):
        self.uri_generator = uri_generator
        self.authenticated_http_client = authenticated_http_client

    def get_resource(self, path: str, uri_params: list[str] = [], query_params: dict = {}) -> Response:
        return self.authenticated_http_client.send_request(
            "GET",
            self.uri_generator.generate(path, uri_params, query_params),
            {"Accept": "*/*"}
        )

    def get_resources(self, path: str, uri_params: list[str] = [], query_params: dict = {}, limit: int = 0) -> Response:
        if limit > 0:
            query_params['limit'] = limit

        query_params['with_count'] = 'true'
        return self.get_resource(path, uri_params, query_params)

    def create_resource(self, path: str, uri_params: list[str] = [], body: JsonSerializable = None) -> Response:
        return self.authenticated_http_client.send_request(
            "POST",
            self.uri_generator.generate(path, uri_params),
            {"Content-Type": "application/json"},
            body
        )

    def upsert_resource(self, path: str, uri_params: list[str] = [], body: JsonSerializable = None) -> Response:
        return self.authenticated_http_client.send_request(
            "PATCH",
            self.uri_generator.generate(path, uri_params),
            {"Content-Type": "application/json"},
            body
        )

    def upsert_list_resource(self, path: str, uri_params: list[str] = [], body: JsonSerializable = None) -> Response:
        return self.authenticated_http_client.send_request(
            "PATCH",
            self.uri_generator.generate(path, uri_params),
            {"Content-Type": "application/vnd.akeneo.collection+json"},
            body
        )

    def upsert_list_json_resource(self, path: str, uri_params: list[str] = [], body: JsonSerializable = None) -> Response:
        return self.authenticated_http_client.send_request(
            "PATCH",
            self.uri_generator.generate(path, uri_params),
            {"Content-Type": "application/json"},
            body
        )

    def delete_resource(self, path: str, uri_params: list[str] = []) -> Response:
        return self.authenticated_http_client.send_request(
            "DELETE",
            self.uri_generator.generate(path, uri_params)
        )
