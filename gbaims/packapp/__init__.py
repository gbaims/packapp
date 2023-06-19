from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from gbaims.packapp import api
from gbaims.packapp.io.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env("FLASK")

    # Compose Object Dependency Graph
    config = Config()  # type: ignore

    # Configure request processing pipeline
    if config.environment.is_production():
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)  # type: ignore

    app.errorhandler(Exception)(api.handle_exception)
    app.get("/fetch_stock")(api.fetch_stock)

    return app
