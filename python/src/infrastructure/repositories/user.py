from typing import Any, Iterable

from src.application.entities.user import User
from src.application.interfaces.user_repo import UserRepo


class UserMem(UserRepo):
    def __init__(self, data: Iterable[dict[str, Any]]) -> None:
        self.data = data

    def list(self) -> list[User]:
        return [User.from_dict(i) for i in self.data]
