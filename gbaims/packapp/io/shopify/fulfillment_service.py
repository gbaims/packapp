from typing import Literal, TypedDict

from gbaims.packapp.io.shopify import Shopify


class _FulfillmentService(TypedDict):
    name: str
    callback_url: str
    inventory_management: bool
    permits_sku_sharing: bool
    fulfillment_orders_opt_in: bool
    tracking_support: bool


class FulfillmentServiceGet(_FulfillmentService):
    id: int
    location_id: int


class FulfillmentServicePost(_FulfillmentService):
    requires_shipping_method: bool
    format: Literal["json"]


_endpoint = "fulfillment_services.json"


class _CreateRequest(TypedDict):
    fulfillment_service: FulfillmentServicePost


class _CreateResponse(TypedDict):
    fulfillment_service: FulfillmentServiceGet


def create(shopify: Shopify, fulfillment_service: FulfillmentServicePost) -> int:
    payload: _CreateRequest = {"fulfillment_service": fulfillment_service}
    response: _CreateResponse = shopify.post(_endpoint, payload=payload)
    return response["fulfillment_service"]["id"]


def find_by_name(shopify: Shopify, name: str) -> FulfillmentServiceGet | None:
    services = all(shopify, name)
    if not services:
        return None
    return services[0]


class _AllResponse(TypedDict):
    fulfillment_services: list[FulfillmentServiceGet]


def all(shopify: Shopify, name: str = "") -> list[FulfillmentServiceGet]:
    response: _AllResponse = shopify.get(_endpoint, params={"scope": "all"})
    services = response["fulfillment_services"]
    if not name:
        return services

    return [s for s in services if s["name"] == name]
