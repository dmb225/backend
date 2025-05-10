from collections.abc import Iterable, Mapping
from typing import Any

from src.application.entities.user import User
from src.application.interfaces.user_repo import UserRepo


class UserMem(UserRepo):
    def __init__(self, data: Iterable[dict[str, Any]]) -> None:
        self.data = data

    def get(self, filters: Mapping[str, Any] | None = None) -> list[User]:
        result = [User.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if "age__eq" in filters:
            result = [r for r in result if r.age == int(filters["age__eq"])]

        if "age__lt" in filters:
            result = [r for r in result if r.age < int(filters["age__lt"])]

        if "age__gt" in filters:
            result = [r for r in result if r.age > int(filters["age__gt"])]

        return result
