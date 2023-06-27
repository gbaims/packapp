from ._client import ShopifyClient
from ._config import ShopifyConfig
from ._errors import ClientShopifyError as ClientShopifyError
from ._errors import ServerShopifyError as ServerShopifyError
from ._errors import ShopifyError as ShopifyError
from ._errors import UnknownShopifyError as UnknownShopifyError
from .endpoints.assigned_fulfillment_order import AssignedFulfillmentOrderEndpoint
from .endpoints.fulfillment import FulfillmentEndpoint
from .endpoints.fulfillment_request import FulfillmentRequestEndpoint
from .endpoints.fulfillment_service import FulfillmentServiceEndpoint
from .endpoints.order import OrderEndpoint


class Shopify:
    def __init__(self, config: ShopifyConfig) -> None:
        self._client = ShopifyClient(config)

    @property
    def assigned_fulfillment_order(self) -> AssignedFulfillmentOrderEndpoint:
        return AssignedFulfillmentOrderEndpoint(self._client)

    @property
    def fulfillment(self) -> FulfillmentEndpoint:
        return FulfillmentEndpoint(self._client)

    @property
    def fulfillment_request(self) -> FulfillmentRequestEndpoint:
        return FulfillmentRequestEndpoint(self._client)

    @property
    def fulfillment_service(self) -> FulfillmentServiceEndpoint:
        return FulfillmentServiceEndpoint(self._client)

    @property
    def order(self) -> OrderEndpoint:
        return OrderEndpoint(self._client)

    def close(self):
        return self._client.close()

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details):  # type: ignore
        self._client.__exit__(*exc_details)  # type: ignore
