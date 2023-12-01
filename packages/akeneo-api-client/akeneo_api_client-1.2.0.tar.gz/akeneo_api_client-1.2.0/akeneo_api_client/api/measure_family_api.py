import json
from collections.abc import Iterable

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination.page_factory import PageFactory
from akeneo_api_client.pagination.resource_cursor import ResourceCursor
from .request.dict_serialize import DictSerialize
from .request.line_serialize import LineSerialize


class MeasureFamilyApi:

    MEASURE_FAMILY_URI = "api/rest/v1/measure-families/%s"
    MEASURE_FAMILIES_URI = "api/rest/v1/measure-families"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.MEASURE_FAMILY_URI, [code])

        return json.loads(response.content)

    def all(self, page_size: int = 100, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(self.MEASURE_FAMILIES_URI, [], query_params, page_size)
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(page_size, page))
