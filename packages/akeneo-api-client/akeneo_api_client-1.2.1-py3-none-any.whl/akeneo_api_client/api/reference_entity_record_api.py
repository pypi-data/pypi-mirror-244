import json
from collections.abc import Iterable
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from akeneo_api_client.pagination.page_factory import PageFactory
from akeneo_api_client.pagination.resource_cursor import ResourceCursor
from .request.dict_serialize import DictSerialize
from .request.list_serialize import ListSerialize


class ReferenceEntityRecordApi:

    REFERENCE_ENTITY_RECORDS_URI = "api/rest/v1/reference-entities/%s/records"
    REFERENCE_ENTITY_RECORD_URI = "api/rest/v1/reference-entities/%s/records/%s"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, reference_entity_code: str, record_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(
            self.REFERENCE_ENTITY_RECORD_URI,
            [reference_entity_code, record_code]
        )

        return json.loads(response.content)

    def all(self, reference_entity_code: str, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(
            self.REFERENCE_ENTITY_RECORDS_URI,
            [reference_entity_code],
            query_params
        )
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(0, page))

    def upsert(self, reference_entity_code: str, record_code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(
            self.REFERENCE_ENTITY_RECORD_URI,
            [reference_entity_code, record_code],
            DictSerialize(data)
        )

    def upsert_list(self, reference_entity_code: str, data: list[dict]) -> list[dict]:
        batch = ListSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_list_json_resource(
            self.REFERENCE_ENTITY_RECORDS_URI,
            [reference_entity_code],
            batch
        )

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
