from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify, fulfillment_service
from gbaims.packapp.io.shopify.fulfillment_service import FulfillmentServicePost


def initialize_data(config: Config):
    _seed_shopify(config)


def _seed_shopify(config: Config):
    with Shopify(config.shopify) as shopify:
        name = config.shopify.fulfillment_service.name
        callback_url = config.shopify.fulfillment_service.callback_url

        if fulfillment_service.find_by_name(shopify, name):
            return

        payload: FulfillmentServicePost = {
            "name": name,
            "callback_url": callback_url,
            "inventory_management": True,
            "permits_sku_sharing": True,
            "fulfillment_orders_opt_in": True,
            "tracking_support": True,
            "requires_shipping_method": True,
            "format": "json",
        }
        fulfillment_service.create(shopify, payload)


if __name__ == "__main__":
    config = Config()  # type: ignore
    initialize_data(config)
