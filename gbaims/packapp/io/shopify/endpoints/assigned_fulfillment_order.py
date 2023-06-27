from typing import Literal, Optional, TypedDict

from .._client import ShopifyClient

AssignmentStatus = Literal[
    "fulfillment_unsubmitted",
    "fulfillment_requested",
    "fulfillment_accepted",
    "cancellation_requested",
]


class Destination(TypedDict):
    id: int
    address1: str
    address2: str
    city: str
    country: str
    email: str
    first_name: str
    last_name: str
    phone: str
    zip: str


class AssignedFulfillmentOrderLineItem(TypedDict):
    id: int
    line_item_id: int
    inventory_item_id: int
    quantity: int


class AssignedFulfillmentOrder(TypedDict):
    id: int
    order_id: int
    assignment_status: AssignmentStatus
    destination: Destination
    line_items: list[AssignedFulfillmentOrderLineItem]


class _AllResponse(TypedDict):
    fulfillment_orders: list[AssignedFulfillmentOrder]


class AssignedFulfillmentOrderEndpoint:
    def __init__(self, client: ShopifyClient) -> None:
        self._client = client

    def all(
        self,
        assignment_status: Optional[AssignmentStatus] = None,
        location_ids: list[int] = [],
    ) -> list[AssignedFulfillmentOrder]:
        endpoint = "assigned_fulfillment_orders.json"
        params: dict[str, str | list[int]] = {}
        if assignment_status:
            params.update({"assignment_status": assignment_status})
        if location_ids:
            params.update({"location_ids[]": location_ids})

        response: _AllResponse = self._client.get(endpoint, params=params)
        return response["fulfillment_orders"]
