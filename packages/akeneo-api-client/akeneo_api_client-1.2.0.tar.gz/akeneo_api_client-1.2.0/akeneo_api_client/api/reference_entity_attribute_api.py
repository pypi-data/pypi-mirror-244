import json
from collections.abc import Iterable
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination.page_factory import PageFactory
from akeneo_api_client.pagination.resource_cursor import ResourceCursor
from .request.dict_serialize import DictSerialize


class ReferenceEntityAttributeApi:

    REFERENCE_ENTITY_ATTRIBUTES_URI = "api/rest/v1/reference-entities/%s/attributes"
    REFERENCE_ENTITY_ATTRIBUTE_URI = "api/rest/v1/reference-entities/%s/attributes/%s"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, reference_entity_code: str, attribute_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.REFERENCE_ENTITY_ATTRIBUTE_URI, [reference_entity_code, attribute_code])

        return json.loads(response.content)

    def all(self, reference_entity_code: str, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(self.REFERENCE_ENTITY_ATTRIBUTES_URI, [reference_entity_code], query_params)
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(0, page))

    def upsert(self, reference_entity_code: str, attribute_code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(
            self.REFERENCE_ENTITY_ATTRIBUTE_URI,
            [reference_entity_code, attribute_code],
            DictSerialize(data)
        )
