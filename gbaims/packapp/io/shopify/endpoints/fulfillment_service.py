from typing import Literal, TypedDict

from .._client import ShopifyClient


class _FulfillmentServiceBase(TypedDict):
    name: str
    callback_url: str
    inventory_management: bool
    permits_sku_sharing: bool
    fulfillment_orders_opt_in: bool
    tracking_support: bool


class FulfillmentService(_FulfillmentServiceBase):
    id: int
    location_id: int


class CreateFulfillmentService(_FulfillmentServiceBase):
    requires_shipping_method: bool
    format: Literal["json"]


class _CreateRequest(TypedDict):
    fulfillment_service: CreateFulfillmentService


class _CreateResponse(TypedDict):
    fulfillment_service: FulfillmentService


class _AllResponse(TypedDict):
    fulfillment_services: list[FulfillmentService]


class FulfillmentServiceEndpoint:
    def __init__(self, client: ShopifyClient) -> None:
        self._client = client
        self._endpoint = "fulfillment_services.json"

    def create(self, fulfillment_service: CreateFulfillmentService) -> int:
        payload: _CreateRequest = {"fulfillment_service": fulfillment_service}
        response: _CreateResponse = self._client.post(self._endpoint, payload=payload)
        return response["fulfillment_service"]["id"]

    def find_by_name(self, name: str) -> FulfillmentService | None:
        if not (services := self.all(name)):
            return None

        return services[0]

    def all(self, name: str = "") -> list[FulfillmentService]:
        params = {"scope": "all"}
        response: _AllResponse = self._client.get(self._endpoint, params=params)
        services = response["fulfillment_services"]
        if not name:
            return services

        return [service for service in services if service["name"] == name]
