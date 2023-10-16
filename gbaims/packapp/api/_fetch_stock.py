import json

from gbaims.packapp import ctx


def fetch_stock():
    bergler = ctx.g.bergler
    requested_sku = ctx.request.args.get("sku")

    with open("downloads/variants.json") as file:
        data = file.read()
    variants = json.loads(data)["variants"]
    if requested_sku:
        variants = [v for v in variants if v["sku"] == requested_sku]
    skus_by_id = {v["inventory_item_id"]: v["sku"] for v in variants}
    availables = bergler.product_available(list(skus_by_id.keys()))
    return {skus_by_id[a["id"]]: a["qty_available"] for a in availables}
