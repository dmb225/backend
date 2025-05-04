from collections.abc import Mapping
from typing import Any, Iterable, Optional

from src.application.entities.user import User
from src.application.interfaces.user_repo import UserRepo


class UserMem(UserRepo):
    def __init__(self, data: Iterable[dict[str, Any]]) -> None:
        self.data = data

    def list(self, filters: Optional[Mapping[str, str]] = None) -> list[User]:
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
