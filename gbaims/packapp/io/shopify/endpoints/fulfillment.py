from typing import TypedDict

from .._client import ShopifyClient


class FulfillmentOrderInfo(TypedDict):
    fulfillment_order_id: int


class CreateFulfillment(TypedDict):
    line_items_by_fulfillment_order: list[FulfillmentOrderInfo]


class _CreateRequest(TypedDict):
    fulfillment: CreateFulfillment


class Fulfillment(TypedDict):
    id: int


class _CreateResponse(TypedDict):
    fulfillment: Fulfillment


class FulfillmentEndpoint:
    def __init__(self, client: ShopifyClient) -> None:
        self._client = client

    def create(self, fulfillment: CreateFulfillment) -> Fulfillment:
        endpoint = "fulfillments.json"
        request: _CreateRequest = {"fulfillment": fulfillment}
        response: _CreateResponse = self._client.post(endpoint, request)
        return response["fulfillment"]
