import json
from collections.abc import Iterable
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination.page_factory import PageFactory
from akeneo_api_client.pagination.resource_cursor import ResourceCursor
from .request.dict_serialize import DictSerialize
from .request.line_serialize import LineSerialize


class FamilyVariantApi:

    FAMILY_VARIANTS_URI = "api/rest/v1/families/%s/variants"
    FAMILY_VARIANT_URI = "api/rest/v1/families/%s/variants/%s"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, family_code: str, family_variant_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(
            self.FAMILY_VARIANT_URI,
            [family_code, family_variant_code]
        )

        return json.loads(response.content)

    def all(self, family_code: str, page_size: int = 10, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(
            self.FAMILY_VARIANTS_URI,
            [family_code],
            query_params,
            page_size
        )
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(page_size, page))

    def upsert(self, family_code: str, family_variant_code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(
            self.FAMILY_VARIANT_URI,
            [family_code, family_variant_code],
            DictSerialize(data)
        )

    def upsert_list(self, family_code: str, data: list[dict]) -> list[dict]:
        batch = LineSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_list_resource(self.FAMILY_VARIANTS_URI, [family_code], batch)

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
