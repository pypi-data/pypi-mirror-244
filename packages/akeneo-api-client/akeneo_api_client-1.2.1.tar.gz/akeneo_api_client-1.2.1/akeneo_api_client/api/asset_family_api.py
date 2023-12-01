import json
from collections.abc import Iterable
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination import (page_factory, resource_cursor)
from .request.dict_serialize import DictSerialize


class AssetFamilyApi:

    ASSET_FAMILIES_URI = "api/rest/v1/asset-families"
    ASSET_FAMILY_URI = "api/rest/v1/asset-families/%s"

    def __init__(
        self,
        resource_client: ResourceClient,
        page_factory: page_factory.PageFactory
    ):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.ASSET_FAMILY_URI, [code])

        return json.loads(response.content)

    def all(self, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(self.ASSET_FAMILIES_URI, [], query_params)
        page = self.page_factory.create_page(response.json())

        return iter(resource_cursor.ResourceCursor(0, page))

    def upsert(self, code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(self.ASSET_FAMILY_URI, [code], DictSerialize(data))
