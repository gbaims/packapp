import logging
import logging.config

from flask import Flask, g
from werkzeug.middleware.proxy_fix import ProxyFix

from gbaims.packapp import api
from gbaims.packapp.io.bergler import Bergler
from gbaims.packapp.io.config import Config
from gbaims.packapp.io.shopify import Shopify


def create_app():
    config = Config()  # type: ignore
    logging.config.dictConfig(config.logging.as_dict())

    app = Flask(__name__)
    app.config.from_prefixed_env("FLASK")
    # app.logger.removeHandler(flask.logging.default_handler)
    # l = logging.getLogger("werkzeug")
    # print(l.handlers)
    # l.info("teste")
    # l.handlers = []
    # print(l.handlers)
    # l.removeHandler(flask.logging.default_handler)
    # print(app.logger.handlers)

    # Compose Object Dependency Graph

    @app.before_request
    def start_resources():  # type: ignore
        g.config = config
        g.bergler = Bergler(config.bergler)
        g.shopify = Shopify(config.shopify)

    @app.teardown_appcontext
    def release_resources(_):  # type: ignore
        g.pop("shopify").close()
        g.pop("bergler")
        g.pop("config")

    # Configure request processing pipeline
    if config.environment.is_production():
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)  # type: ignore

    # logconfig_dict = {"version": 1, "root": {"level": "DEBUG"}, "loggers": {"gunicorn": {"level": "DEBUG"}}}
    #     gunicorn_logger = logging.getLogger("gunicorn.error")
    #     root_logger = logging.getLogger()
    #     root_logger.handlers = gunicorn_logger.handlers
    #     root_logger.setLevel(gunicorn_logger.level)
    # else:
    #     root_logger = logging.getLogger()
    #     root_logger.addHandler(flask.logging.default_handler)  # type: ignore
    #     root_logger.setLevel(app.logger.level)

    app.errorhandler(Exception)(api.handle_exception)
    app.get("/fetch_stock.json")(api.fetch_stock)
    app.post("/fulfillment_order_notification")(api.fulfillment_order_notification)

    return app
