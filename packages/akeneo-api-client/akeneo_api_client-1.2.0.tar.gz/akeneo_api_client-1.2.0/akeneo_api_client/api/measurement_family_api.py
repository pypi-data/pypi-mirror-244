import json

from akeneo_api_client.client.resource_client import ResourceClient
from .request.list_serialize import ListSerialize


class MeasurementFamilyApi:

    MEASUREMENT_FAMILIES_URI = "api/rest/v1/measurement-families"

    def __init__(self, resource_client: ResourceClient):
        self.resource_client = resource_client

    def all(self) -> list:
        response = self.resource_client.get_resource(self.MEASUREMENT_FAMILIES_URI)

        return response.json()

    def upsert_list(self, data: list[dict]) -> list[dict]:
        batch = ListSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_list_resource(self.MEASUREMENT_FAMILIES_URI, [], batch)

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
