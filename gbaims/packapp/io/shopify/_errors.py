from requests import Request, Response

from gbaims.packapp.lib.errors import PackappError


class ShopifyError(PackappError):
    pass


class ServerShopifyError(ShopifyError):
    message = "Shopify server failed to handle an apparently valid request [{code} {reason}] {body}"

    def __init__(self, code: int, reason: str, body: str) -> None:
        super().__init__(code=code, reason=reason, body=body)


class ClientShopifyError(ShopifyError):
    message = "The request could not be fulfilled by Shopify servers [{code} {reason}] {body}"

    def __init__(self, code: int, reason: str, body: str) -> None:
        super().__init__(code=code, reason=reason, body=body)


class UnknownShopifyError(ShopifyError):
    message = "An unknown error has ocurred while trying to connect to Shopify"

    def __init__(self, request: Request, response: Response) -> None:
        super().__init__(request=request, response=response)
