import json

from flask import abort, request


def fetch_stock():
    with open("downloads/skudb.json") as file:
        data = file.read()

    skus = json.loads(data)
    requested_sku = request.args.get("sku")
    if requested_sku:
        if (qty := skus.get(requested_sku)) is None:
            abort(404)

        return {requested_sku: qty}

    return skus
