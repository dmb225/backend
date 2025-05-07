import dataclasses
import uuid
from typing import Any


@dataclasses.dataclass
class User:
    id: uuid.UUID
    name: str
    age: int

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "User":
        return cls(**d)

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
