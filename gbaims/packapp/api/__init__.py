import logging

from flask import json
from werkzeug import Response
from werkzeug.exceptions import HTTPException, InternalServerError

from ._fetch_stock import *
from ._fulfillment_order_notification import *


def handle_exception(exc: Exception) -> Response:
    logger = logging.getLogger(__name__)
    logger.exception(exc)

    error = exc if isinstance(exc, HTTPException) else InternalServerError()
    data = {
        "code": error.code,
        "name": error.name,
        "description": error.description,
    }

    response = error.get_response()  # type: ignore
    response.content_type = "application/json"
    response.data = json.dumps(data)  # type: ignore
    return response  # type: ignore
