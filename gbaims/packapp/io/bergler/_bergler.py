from gbaims.packapp.api._fulfillment_order_notification import Deliverable
from gbaims.packapp.io.bergler.methods.order_import import order_import
from gbaims.packapp.io.bergler.methods.product_available import (
    ProductAvailable,
    product_available,
)

from ._client import BerglerClient
from ._config import BerglerConfig


class Bergler:
    def __init__(self, config: BerglerConfig) -> None:
        self._client = BerglerClient(config)

    def product_available(self, ids: list[int]) -> list[ProductAvailable]:
        return product_available(self._client, ids)

    def order_import(self, deliverable: Deliverable):
        return order_import(self._client, deliverable)
