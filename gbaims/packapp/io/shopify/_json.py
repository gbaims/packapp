from datetime import date, datetime, time
from json import JSONDecoder, JSONEncoder
from typing import Any


class ShopifyJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(object_hook=self.hook, *args, **kwargs)

    def hook(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {key: self.hook(value) for key, value in obj.items()}  # type: ignore
        if isinstance(obj, list):
            return [self.hook(value) for value in obj]  # type: ignore
        if isinstance(obj, str):
            try:
                return datetime.fromisoformat(obj)
            except ValueError:
                pass
        return obj


class ShopifyJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        return super().default(o)
