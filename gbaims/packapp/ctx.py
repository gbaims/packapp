import flask

from gbaims.packapp.io.bergler import Bergler
from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify


class _G:
    @property
    def config(self) -> Config:
        return flask.g.config

    @property
    def bergler(self) -> Bergler:
        return flask.g.bergler

    @property
    def shopify(self) -> Shopify:
        return flask.g.shopify


g = _G()
app = flask.current_app
request = flask.request
