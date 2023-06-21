class ShopifyError(Exception):
    pass


class ServerShopifyError(ShopifyError):
    pass


class ClientShopifyError(ShopifyError):
    pass


class NotFoundShopifyError(ClientShopifyError):
    pass
