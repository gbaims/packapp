import math
from datetime import datetime
from typing import Tuple, TypedDict

from flask import abort

from gbaims.packapp import ctx
from gbaims.packapp.core.errors import InconsistencyError, ValidationError

# from gbaims.packapp.errors import InconsistentDataError, PackappError, ValidationError
from gbaims.packapp.io.bergler.errors import BerglerError
from gbaims.packapp.io.bergler.methods.product_available import ProductAvailable
from gbaims.packapp.io.shopify import ShopifyError
from gbaims.packapp.io.shopify.endpoints.assigned_fulfillment_order import (
    AssignedFulfillmentOrder,
    AssignedFulfillmentOrderLineItem,
)
from gbaims.packapp.io.shopify.endpoints.fulfillment import CreateFulfillment
from gbaims.packapp.io.shopify.endpoints.order import Order, OrderLineItem


def fulfillment_order_notification() -> Tuple[dict[str, str], int]:
    kind = str(ctx.request.json.get("kind", "")).lower() if ctx.request.json is not None else ""
    match kind:
        case "fulfillment_request":
            _fulfillment()
        case "cancellation_request":
            return abort(501)  # TODO: _cancellation
        case _:
            return abort(422)

    return {}, 200


def _fulfillment():
    shopify = ctx.g.shopify

    name = ctx.g.config.shopify.fulfillment_service.name
    if not (service := shopify.fulfillment_service.find_by_name(name)):
        raise InconsistencyError("Fulfillment Service", name)

    # Get all Fulfillment Orders with requested fulfillment to this fulfillment service location
    location_ids = [service["location_id"]]
    fulfillment_orders = shopify.assigned_fulfillment_order.all("fulfillment_requested", location_ids)

    for fulfillment_order in fulfillment_orders:
        _process_fulfillment_order(fulfillment_order)


def _process_fulfillment_order(fulfillment_order: AssignedFulfillmentOrder):
    shopify = ctx.g.shopify
    bergler = ctx.g.bergler

    try:
        order = shopify.order.find(fulfillment_order["order_id"])
    except ShopifyError as exc:
        shopify.fulfillment_request.reject(fulfillment_order["id"])
        raise exc

    try:
        deliverable = _create_deliverable(order, fulfillment_order)
    except (InconsistencyError, ValidationError) as exc:
        shopify.fulfillment_request.reject(fulfillment_order["id"])
        if isinstance(exc, InconsistencyError):
            raise exc
        return
    else:
        items = deliverable["items"]
        items_ids = [item["inventory_item_id"] for item in items]
        availables = bergler.product_available(items_ids)
        if _unavailables := _unavailable_items(items, availables):
            shopify.fulfillment_request.reject(deliverable["fulfillment_order_id"])
            return

        try:
            bergler.order_import(deliverable)
        except BerglerError:
            shopify.fulfillment_request.reject(deliverable["fulfillment_order_id"])
            return
            # TODO return or raise

        shopify.fulfillment_request.accept(deliverable["fulfillment_order_id"])

        # Create fulfillment back in shopify
        fulfillment: CreateFulfillment = {
            "line_items_by_fulfillment_order": [{"fulfillment_order_id": deliverable["fulfillment_order_id"]}]
        }
        shopify.fulfillment.create(fulfillment)
        # TODO: Se der errado, cancelar ou fechar o fulfillment order que foi aceito


class DeliverableItem(TypedDict):
    id: int
    inventory_item_id: int
    sku: str
    quantity: int
    price: float


class DeliverableAddress(TypedDict):
    name: str
    street: str
    street2: str
    country_code: str
    postal_code: str
    city: str
    phone: str
    email: str


class Deliverable(TypedDict):
    id: int
    fulfillment_order_id: int
    customer_id: int
    number: str
    date: datetime
    net_amount: float
    gross_amount: float
    items: list[DeliverableItem]
    shipping_address: DeliverableAddress
    billing_address: DeliverableAddress


def _create_deliverable(order: Order, fulfillment_order: AssignedFulfillmentOrder) -> Deliverable:
    if order["id"] != fulfillment_order["order_id"]:
        raise InconsistencyError("Order ID", order["id"])

    fields_with_length_limit = [
        order["shipping_address"]["name"],
        order["shipping_address"]["address1"],
        order["shipping_address"]["address2"],
        order["billing_address"]["name"],
        order["billing_address"]["address1"],
        order["billing_address"]["address2"],
    ]
    if any(map(lambda f: len(str(f)) > 50, fields_with_length_limit)):
        raise ValidationError(f"Name or Address Information have more than 50 characters")

    def to_deliverable_item(fulfillment_order_item: AssignedFulfillmentOrderLineItem) -> DeliverableItem:
        def is_current_item(order_item: OrderLineItem):
            return order_item["id"] == fulfillment_order_item["line_item_id"]

        order_item = next(filter(is_current_item, order["line_items"]))
        return {
            "id": fulfillment_order_item["id"],
            "inventory_item_id": fulfillment_order_item["inventory_item_id"],
            "quantity": fulfillment_order_item["quantity"],
            "sku": order_item["sku"],
            "price": float(order_item["price"]),
        }

    return {
        "id": order["id"],
        "fulfillment_order_id": fulfillment_order["id"],
        "customer_id": order["customer"]["id"],
        "number": order["name"],
        "date": order["created_at"],
        "net_amount": float(order["total_price"]) - float(order["total_tax"]),
        "gross_amount": float(order["total_price"]),
        "items": list(map(to_deliverable_item, fulfillment_order["line_items"])),
        "shipping_address": {
            "name": order["shipping_address"]["name"],
            "street": order["shipping_address"]["address1"],
            "street2": order["shipping_address"]["address2"] or "",
            "country_code": order["shipping_address"]["country_code"],
            "postal_code": order["shipping_address"]["zip"],
            "city": order["shipping_address"]["city"],
            "phone": order["shipping_address"]["phone"],
            "email": fulfillment_order["destination"]["email"],
        },
        "billing_address": {
            "name": order["billing_address"]["name"],
            "street": order["billing_address"]["address1"],
            "street2": order["billing_address"]["address2"] or "",
            "country_code": order["billing_address"]["country_code"],
            "postal_code": order["billing_address"]["zip"],
            "city": order["billing_address"]["city"],
            "phone": order["billing_address"]["phone"],
            "email": fulfillment_order["destination"]["email"],
        },
    }


def _unavailable_items(
    items: list[DeliverableItem], availables: list[ProductAvailable]
) -> list[DeliverableItem]:
    lookup = {available["id"]: available["qty_available"] for available in availables}
    unavailables: list[DeliverableItem] = []
    for item in items:
        try:
            qty = item["quantity"]
            qty_available = lookup[item["inventory_item_id"]]
        except KeyError:
            unavailables.append(item)
        else:
            if not math.isclose(qty, qty_available) and qty > qty_available:
                unavailables.append(item)
    return unavailables
