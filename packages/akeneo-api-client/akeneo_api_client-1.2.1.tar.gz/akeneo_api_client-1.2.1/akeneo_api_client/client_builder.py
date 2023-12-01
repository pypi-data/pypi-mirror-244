from .security.authentication import Authentication
from .client.uri_generator import UriGenerator
from .client.http_client import HttpClient
from .client.resource_client import ResourceClient
from .client.authenticated_http_client import AuthenticatedHttpClient
from .pagination.page_factory import PageFactory
from .akeneo_client import AkeneoClient
from .api import (asset_api,
                  asset_attribute_api,
                  asset_attribute_option_api,
                  asset_family_api,
                  attribute_api,
                  attribute_group_api,
                  attribute_option_api,
                  authentication_api,
                  category_api,
                  channel_api,
                  currency_api,
                  family_api,
                  family_variant_api,
                  locale_api,
                  measure_family_api,
                  measurement_family_api,
                  product_model_api,
                  product_uuid_api,
                  reference_entity_api,
                  reference_entity_attribute_api,
                  reference_entity_attribute_option_api,
                  reference_entity_record_api)


class ClientBuilder:

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def build_authenticated_by_password(self, username, password, client_id, secret) -> AkeneoClient:
        authentication = Authentication.from_password(username, password, client_id, secret)
        return self.build(authentication)

    def build_authenticated_by_token(self, client_id, secret, token, refresh_token) -> AkeneoClient:
        authentication = Authentication.from_token(client_id, secret, token, refresh_token)
        return self.build(authentication)

    def build(self, authentication) -> AkeneoClient:
        uri_generator = UriGenerator(self.base_uri)
        http_client = HttpClient()

        authenticated_http_client = AuthenticatedHttpClient(
            http_client,
            authentication,
            authentication_api.AuthenticationApi(http_client, uri_generator)
        )

        resource_client = ResourceClient(uri_generator, authenticated_http_client)
        page_factory = PageFactory(authenticated_http_client)

        return AkeneoClient(
            authentication=authentication,
            _asset_api=asset_api.AssetApi(resource_client, page_factory),
            _asset_attribute_api=asset_attribute_api.AssetAttributeApi(resource_client),
            _asset_attribute_option_api=asset_attribute_option_api.AssetAttributeOptionApi(resource_client),
            _asset_family_api=asset_family_api.AssetFamilyApi(resource_client, page_factory),
            _attribute_api=attribute_api.AttributeApi(resource_client, page_factory),
            _attribute_group_api=attribute_group_api.AttributeGroupApi(resource_client, page_factory),
            _attribute_option_api=attribute_option_api.AttributeOptionApi(resource_client, page_factory),
            _category_api=category_api.CategoryApi(resource_client, page_factory),
            _channel_api=channel_api.ChannelApi(resource_client, page_factory),
            _currency_api=currency_api.CurrencyApi(resource_client, page_factory),
            _family_api=family_api.FamilyApi(resource_client, page_factory),
            _family_variant_api=family_variant_api.FamilyVariantApi(resource_client, page_factory),
            _locale_api=locale_api.LocaleApi(resource_client, page_factory),
            _measure_family_api=measure_family_api.MeasureFamilyApi(resource_client, page_factory),
            _measurement_family_api=measurement_family_api.MeasurementFamilyApi(resource_client),
            _product_model_api=product_model_api.ProductModelApi(resource_client, page_factory),
            _product_uuid_api=product_uuid_api.ProductUuidApi(resource_client, page_factory),
            _reference_entity_api=reference_entity_api.ReferenceEntityApi(resource_client, page_factory),
            _reference_entity_attribute_api=reference_entity_attribute_api.ReferenceEntityAttributeApi(resource_client, page_factory),
            _reference_entity_attribute_option_api=reference_entity_attribute_option_api.ReferenceEntityAttributeOptionApi(resource_client),
            _reference_entity_record_api=reference_entity_record_api.ReferenceEntityRecordApi(resource_client, page_factory)
        )
