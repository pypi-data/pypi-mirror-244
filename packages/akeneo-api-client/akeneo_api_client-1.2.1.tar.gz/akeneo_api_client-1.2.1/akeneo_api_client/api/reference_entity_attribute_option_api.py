import json
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from .request.dict_serialize import DictSerialize


class ReferenceEntityAttributeOptionApi:

    REFERENCE_ENTITY_ATTRIBUTE_OPTIONS_URI = "api/rest/v1/reference-entities/%s/attributes/%s/options"
    REFERENCE_ENTITY_ATTRIBUTE_OPTION_URI = "api/rest/v1/reference-entities/%s/attributes/%s/options/%s"

    def __init__(self, resource_client: ResourceClient):
        self.resource_client = resource_client

    def get(self, reference_entity_code: str, attribute_code: str, attribute_option_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(
            self.REFERENCE_ENTITY_ATTRIBUTE_OPTION_URI,
            [reference_entity_code, attribute_code, attribute_option_code]
        )

        return json.loads(response.content)

    def all(self, reference_entity_code: str, attribute_code: str) -> list[dict]:
        response = self.resource_client.get_resources(
            self.REFERENCE_ENTITY_ATTRIBUTE_OPTIONS_URI,
            [reference_entity_code, attribute_code]
        )

        return response.json()

    def upsert(
        self,
        reference_entity_code: str,
        attribute_code: str,
        attribute_option_code: str,
        data: dict = {}
    ) -> Response:
        return self.resource_client.upsert_resource(
            self.REFERENCE_ENTITY_ATTRIBUTE_OPTION_URI,
            [reference_entity_code, attribute_code, attribute_option_code],
            DictSerialize(data)
        )
