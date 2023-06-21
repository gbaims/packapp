from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify
from gbaims.packapp.io.shopify.endpoints.fulfillment_service import (
    CreateFulfillmentService,
)


def initialize_data(config: Config):
    _seed_shopify(config)


def _seed_shopify(config: Config):
    with Shopify(config.shopify) as shopify:
        name = config.shopify.fulfillment_service.name
        callback_url = config.shopify.fulfillment_service.callback_url

        if shopify.fulfillment_service.find_by_name(name):
            return

        payload: CreateFulfillmentService = {
            "name": name,
            "callback_url": callback_url,
            "inventory_management": True,
            "permits_sku_sharing": True,
            "fulfillment_orders_opt_in": True,
            "tracking_support": True,
            "requires_shipping_method": True,
            "format": "json",
        }
        shopify.fulfillment_service.create(payload)


if __name__ == "__main__":
    config = Config()  # type: ignore
    initialize_data(config)
