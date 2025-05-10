from collections.abc import Mapping
from typing import Any, Protocol

from src.application.entities.user import User


class UserRepo(Protocol):
    def get(self, filters: Mapping[str, Any] | None = None) -> list[User]: ...
