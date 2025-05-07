import json
from typing import Any


class UserJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            to_serialize = {
                "id": str(o.id),
                "name": o.name,
                "age": o.age,
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)
