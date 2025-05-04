from collections.abc import Mapping
from typing import Optional, Protocol

from src.application.entities.user import User


class UserRepo(Protocol):
    def list(self, filters: Optional[Mapping[str, str]] = None) -> list[User]: ...
