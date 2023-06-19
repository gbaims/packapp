from flask import json
from werkzeug import Response
from werkzeug.exceptions import HTTPException, InternalServerError

from ._fetch_stock import *


def handle_exception(e: Exception) -> Response:
    error = e if isinstance(e, HTTPException) else InternalServerError()
    data = {
        "code": error.code,
        "name": error.name,
        "description": error.description,
    }

    response = error.get_response()  # type: ignore
    response.content_type = "application/json"
    response.data = json.dumps(data)  # type: ignore
    return response  # type: ignore
