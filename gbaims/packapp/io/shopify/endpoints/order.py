from datetime import datetime
from typing import Optional, TypedDict

from .._client import ShopifyClient, ShopifyFallible
from .._exceptions import ShopifyFailure


class Customer(TypedDict):
    id: int


class Address(TypedDict):
    name: str
    phone: str
    address1: str
    address2: Optional[str]
    city: str
    country_code: str
    zip: str


class OrderLineItem(TypedDict):
    id: int
    sku: str
    price: str


class Order(TypedDict):
    id: int
    name: str
    customer: Customer
    billing_address: Address
    shipping_address: Address
    line_items: list[OrderLineItem]
    created_at: datetime
    total_price: str
    total_tax: str


class _FindResponse(TypedDict):
    order: Order


class OrderEndpoint:
    def __init__(self, client: ShopifyClient) -> None:
        self._client = client

    def find(self, id: int) -> ShopifyFallible[Order]:
        endpoint = f"orders/{id}.json"
        response: ShopifyFallible[_FindResponse] = self._client.get(endpoint)
        if isinstance(response, ShopifyFailure):
            return response
        return response["order"]
