import json
from requests.models import Response

from akeneo_api_client.client.resource_client import ResourceClient
from .request.dict_serialize import DictSerialize


class AssetAttributeApi:

    ASSET_ATTRIBUTES_URI = "api/rest/v1/asset-families/%s/attributes"
    ASSET_ATTRIBUTE_URI = "api/rest/v1/asset-families/%s/attributes/%s"

    def __init__(self, resource_client: ResourceClient):
        self.resource_client = resource_client

    def get(self, asset_family_code: str, attribute_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.ASSET_ATTRIBUTE_URI, [asset_family_code, attribute_code])

        return json.loads(response.content)

    def all(self, asset_family_code: str) -> list:
        response = self.resource_client.get_resources(self.ASSET_ATTRIBUTES_URI, [asset_family_code])
        return json.loads(response.content)

    def upsert(self, asset_family_code: str, attribute_code: str, data: dict = {}) -> Response:
        return self.resource_client.upsert_resource(
            self.ASSET_ATTRIBUTE_URI,
            [asset_family_code, attribute_code],
            DictSerialize(data)
        )
