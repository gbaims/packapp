import json
from typing import Any, Mapping

from requests import Response, Session
from requests.adapters import HTTPAdapter

from gbaims.packapp.io.config import ShopifyConfig


class Shopify:
    def __init__(self, config: ShopifyConfig) -> None:
        self._base_url = f"https://{config.host}/admin/api/2023-04/"
        self._token = config.token
        self._session: Session | None = None

    def close(self):
        if self._session is not None:
            self._session.close()

    def get(self, endpoint: str, params: dict[str, str] | None = None) -> Any:
        response = self._request("GET", endpoint, params=params)
        return response.json()

    def post(self, endpoint: str, payload: Mapping[str, object] | None = None) -> Any:
        data = json.dumps(payload)
        response = self._request("POST", endpoint, data=data)
        return response.json()

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        url = f"{self._base_url}{endpoint}"
        # TODO: Handle bad responses and exceptions
        return self._lazy_session().request(method, url, **kwargs)

    def _lazy_session(self) -> Session:
        if self._session is not None:
            return self._session

        headers = {
            "X-Shopify-Access-Token": self._token,
            "Content-Type": "application/json",
        }

        self._session = Session()
        self._session.headers.update(headers)
        self._session.mount(self._base_url, HTTPAdapter(max_retries=3))
        return self._session

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):  # type: ignore
        self.close()
