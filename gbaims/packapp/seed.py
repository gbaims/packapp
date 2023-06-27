from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify, ShopifyConfig, ShopifyFailure
from gbaims.packapp.io.shopify.endpoints.fulfillment_service import (
    CreateFulfillmentService,
)


def initialize_data(config: Config):
    _seed_shopify(config.shopify)


def _seed_shopify(config: ShopifyConfig):
    with Shopify(config) as shopify:
        name = config.fulfillment_service.name
        callback_url = config.fulfillment_service.callback_url

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
        service = shopify.fulfillment_service.create(payload)
        if isinstance(service, ShopifyFailure):
            raise service


if __name__ == "__main__":
    config = Config()  # type: ignore
    initialize_data(config)
