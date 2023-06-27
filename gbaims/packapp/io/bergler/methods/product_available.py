from typing import TypedDict

# from .._utils import float_with_comma
from .. import utils as utils
from .._client import BerglerClient


class ProductAvailable(TypedDict):
    id: int
    qty_available: float


def product_available(bergler: BerglerClient, ids: list[int]) -> list[ProductAvailable]:
    if not ids:
        return []

    payload = _create_payload(ids)
    response = bergler.post("WebShopProductAvailable", payload)
    products = response.Products.Product  # Response come with a list of Product Element

    return [
        {
            "id": int(product.YourProductID.cdata),
            "qty_available": utils.from_german_separator(product.AvailableQuantity.cdata),
        }
        for product in products
    ]


def _create_payload(ids: list[int]) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        "<Products>"
        f"""{"".join([( 
            "<Product>"
                f"<ProductID>{id}</ProductID>" 
            "</Product>"
        ) for id in ids])}"""
        "</Products>"
    )
