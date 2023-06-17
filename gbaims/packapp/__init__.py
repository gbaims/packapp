from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def root():
        return {"hello": "world"}

    return app
