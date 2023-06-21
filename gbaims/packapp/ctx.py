import flask

from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify


class _G:
    @property
    def config(self) -> Config:
        return flask.g.config

    @property
    def shopify(self) -> Shopify:
        return flask.g.shopify


g = _G()
request = flask.request
