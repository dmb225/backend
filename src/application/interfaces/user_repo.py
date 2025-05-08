from collections.abc import Mapping
from typing import Any, Optional, Protocol

from src.application.entities.user import User


class UserRepo(Protocol):
    def get(self, filters: Optional[Mapping[str, Any]] = None) -> list[User]: ...
