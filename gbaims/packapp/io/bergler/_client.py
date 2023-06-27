import logging
from typing import Literal

import untangle
from suds import WebFault  # type: ignore
from suds.client import Client  # type: ignore
from untangle import Element

from gbaims.packapp.io.bergler.errors import (
    ClientBerglerError,
    InvalidOrForbiddenBerglerError,
    ServerBerglerError,
    UnknownBerglerError,
)

from ._config import BerglerConfig

Method = Literal[
    "WebShopProductImport",
    "WebShopProductAvailable",
    "WebShopOrderImport",
    "WebShopOrderState",
]


class BerglerClient:
    def __init__(self, config: BerglerConfig) -> None:
        self._config = config
        self._client: Client | None = None

    def post(self, method: Method, payload: str) -> Element:
        logger = logging.getLogger(__name__)
        try:
            logger.debug(f"Method: {method}\n\nPayload:\n{payload}")
            service = self._lazy_client().service
            reply = service.gbCallCustomerBusinessLinkMethod(
                self._config.access_area,
                self._config.customer_number,
                self._config.password,
                method,
                payload,
            )
            logger.debug(f"Reply: {reply}")
        except WebFault as exc:
            raise ServerBerglerError(exc.fault, exc.document) from exc
        else:
            if not reply.gbCallCustomerBusinessLinkMethodResult:
                raise InvalidOrForbiddenBerglerError(reply.sResult)
            result = untangle.parse(reply.sResult)
            if result.Response.State.cdata == "Fail":
                code = result.Response.ErrorCode.cdata
                message = result.Response.Message.cdata
                raise ClientBerglerError(code, message)
            if result.Response.State.cdata != "Successfull":
                raise UnknownBerglerError(reply.sResult)

            return result.Response

    def _lazy_client(self) -> Client:
        if self._client is not None:
            return self._client

        self._client = Client(self._config.url)
        return self._client


# (reply){
#    gbCallCustomerBusinessLinkMethodResult = False
#    sResult = "Der angegebene Zugang ist nicht freigegeben."
#  }

# (reply){
#    gbCallCustomerBusinessLinkMethodResult = True
#    sResult = "<?xml version="1.0" encoding="utf-8" ?><Response><State>Fail</State><Message><![CDATA[unbekannter Artikel 99999996]]></Message><ErrorCode>2002</ErrorCode></Response>"
#  }

# (reply){
#    gbCallCustomerBusinessLinkMethodResult = True
#    sResult = "<?xml version="1.0" encoding="utf-8" ?><Response><State>Successfull</State><Products><Product><ProductID>154078</ProductID><YourProductID>99999998</YourProductID><AvailableQuantity>0,0000</AvailableQuantity><StockQuantity>0,0000</StockQuantity></Product></Products></Response>"
