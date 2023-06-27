import json
from typing import Any, Mapping, Optional, TypeVar

from requests import HTTPError, RequestException, Response, Session
from requests.adapters import HTTPAdapter

from ._config import ShopifyConfig
from ._exceptions import (
    ClientShopifyError,
    ServerShopifyFailure,
    ShopifyFailure,
    UnknownShopifyError,
)
from ._json import ShopifyJSONDecoder, ShopifyJSONEncoder

T = TypeVar("T")
ShopifyFallible = T | ServerShopifyFailure


class ShopifyClient:
    def __init__(self, config: ShopifyConfig) -> None:
        self._config = config
        self._session: Optional[Session] = None

    def get(self, endpoint: str, params: Optional[Mapping[str, Any]] = None) -> ShopifyFallible[T]:
        response = self._request("GET", endpoint, params=params)
        if isinstance(response, ShopifyFailure):
            return response
        return response.json(cls=ShopifyJSONDecoder)

    def post(self, endpoint: str, payload: Optional[Mapping[str, Any]] = None) -> ShopifyFallible[T]:
        data = json.dumps(payload, cls=ShopifyJSONEncoder)
        response = self._request("POST", endpoint, data=data)
        if isinstance(response, ShopifyFailure):
            return response
        return response.json(cls=ShopifyJSONDecoder)

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> ShopifyFallible[Response]:
        url = f"{self._config.base_url}{endpoint}"
        try:
            response = self._lazy_session().request(method, url, **kwargs)
            response.raise_for_status()
        except HTTPError as exc:
            code = exc.response.status_code
            reason = exc.response.reason
            body = exc.response.text
            if 400 <= code < 500:
                raise ClientShopifyError(code, reason, body) from exc
            return ServerShopifyFailure(code, reason, body)
        except RequestException as exc:
            request = exc.request
            response = exc.response
            raise UnknownShopifyError(request, response) from exc
        else:
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
