from typing import Literal, Optional, TypedDict

from typing_extensions import NotRequired

from .._client import ShopifyClient, ShopifyFallible
from .._exceptions import ShopifyFailure


class AcceptedFulfillmentOrder(TypedDict):
    id: int
    request_status: Literal["accepted"]


class _AcceptResponse(TypedDict):
    fulfillment_order: AcceptedFulfillmentOrder


class RejectFulfillmentRequestLineItem(TypedDict):
    fulfillment_order_line_item_id: int
    message: str


class RejectFulfillmentRequest(TypedDict):
    line_items: NotRequired[list[RejectFulfillmentRequestLineItem]]
    message: NotRequired[str]
    reason: NotRequired[
        Literal[
            "incorrect_address",
            "inventory_out_of_stock",
            "ineligible_product",
            "undeliverable_destination",
            "other",
        ]
    ]


class _RejectRequest(TypedDict):
    fulfillment_request: NotRequired[RejectFulfillmentRequest]


class RejectedFulfillmentOrder(TypedDict):
    id: int
    request_status: Literal["rejected"]


class _RejectResponse(TypedDict):
    fulfillment_order: RejectedFulfillmentOrder


class FulfillmentRequestEndpoint:
    def __init__(self, client: ShopifyClient) -> None:
        self._client = client

    def accept(self, fulfillment_order_id: int) -> ShopifyFallible[AcceptedFulfillmentOrder]:
        endpoint = f"fulfillment_orders/{fulfillment_order_id}/fulfillment_request/accept.json"
        response: ShopifyFallible[_AcceptResponse] = self._client.post(endpoint)
        if isinstance(response, ShopifyFailure):
            return response
        return response["fulfillment_order"]
        # TODO handle unsuccessful response

    def reject(
        self, fulfillment_order_id: int, fulfillment_request: Optional[RejectFulfillmentRequest] = None
    ) -> ShopifyFallible[RejectedFulfillmentOrder]:
        endpoint = f"fulfillment_orders/{fulfillment_order_id}/fulfillment_request/reject.json"
        request: _RejectRequest = {"fulfillment_request": fulfillment_request} if fulfillment_request else {}
        response: ShopifyFallible[_RejectResponse] = self._client.post(endpoint, request)
        if isinstance(response, ShopifyFailure):
            return response
        return response["fulfillment_order"]
