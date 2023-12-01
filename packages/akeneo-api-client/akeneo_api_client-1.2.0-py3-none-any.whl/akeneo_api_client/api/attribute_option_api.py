import json
from collections.abc import Iterable
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination.page_factory import PageFactory
from akeneo_api_client.pagination.resource_cursor import ResourceCursor
from .request.dict_serialize import DictSerialize
from .request.line_serialize import LineSerialize


class AttributeOptionApi:

    ATTRIBUTE_OPTIONS_URI = "api/rest/v1/attributes/%s/options"
    ATTRIBUTE_OPTION_URI = "api/rest/v1/attributes/%s/options/%s"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, attribute_code: str, code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.ATTRIBUTE_OPTION_URI, [attribute_code, code])

        return json.loads(response.content)

    def all(self, attribute_code: str, page_size: int = 10, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(
            self.ATTRIBUTE_OPTIONS_URI,
            [attribute_code],
            query_params,
            page_size
        )
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(page_size, page))

    def create(self, attribute_code: str, attribute_option_code: str, data: dict = {}) -> Response:
        data["code"] = attribute_option_code
        data["attribute"] = attribute_code

        return self.resource_client.create_resource(
            self.ATTRIBUTE_OPTIONS_URI,
            [attribute_code],
            DictSerialize(data)
        )

    def upsert(self, attribute_code: str, attribute_option_code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(
            self.ATTRIBUTE_OPTION_URI,
            [attribute_code, attribute_option_code],
            DictSerialize(data)
        )

    def upsert_list(self, attribute_code: str, data: list[dict]) -> list[dict]:
        batch = LineSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_list_resource(self.ATTRIBUTE_OPTIONS_URI, [attribute_code], batch)

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
