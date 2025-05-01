import dataclasses
import uuid


@dataclasses.dataclass
class User:
    id: uuid.UUID
    name: str
    age: int

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
