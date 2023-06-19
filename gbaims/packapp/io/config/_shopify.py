from pydantic import BaseModel


class FulfillmentServiceConfig(BaseModel):
    name: str
    callback_url: str


class ShopifyConfig(BaseModel):
    host: str
    token: str
    fulfillment_service: FulfillmentServiceConfig
