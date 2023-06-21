import json
from typing import Any, Mapping, Optional

from requests import RequestException, Response, Session
from requests.adapters import HTTPAdapter

from ._config import ShopifyConfig
from ._errors import (
    ClientShopifyError,
    NotFoundShopifyError,
    ServerShopifyError,
    ShopifyError,
)
from ._json import ShopifyJSONDecoder, ShopifyJSONEncoder


class ShopifyClient:
    def __init__(self, config: ShopifyConfig) -> None:
        self._config = config
        self._session: Optional[Session] = None

    def get(self, endpoint: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        response = self._request("GET", endpoint, params=params)
        return response.json(cls=ShopifyJSONDecoder)

    def post(self, endpoint: str, payload: Optional[Mapping[str, Any]] = None) -> Any:
        data = json.dumps(payload, cls=ShopifyJSONEncoder)
        response = self._request("POST", endpoint, data=data)
        return response.json(cls=ShopifyJSONDecoder)

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        url = f"{self._config.base_url}{endpoint}"
        try:
            response = self._lazy_session().request(method, url, **kwargs)
        except RequestException as re:
            raise ShopifyError("Error raised by requests package") from re
        else:
            code = response.status_code
            reason = response.reason
            if code == 404:
                raise NotFoundShopifyError(code, reason, response)
            elif 400 <= code < 500:
                raise ClientShopifyError(code, reason, response)
            elif 500 <= code < 600:
                raise ServerShopifyError(code, reason, response)
            return response

    def _lazy_session(self) -> Session:
        if self._session is not None:
            return self._session

        headers = {
            "X-Shopify-Access-Token": self._config.token,
            "Content-Type": "application/json",
        }
        self._session = Session()
        self._session.headers.update(headers)
        self._session.mount(self._config.base_url, HTTPAdapter(max_retries=3))
        return self._session

    def close(self):
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):  # type: ignore
        self.close()
