from typing import Protocol

from src.application.entities.user import User


class UserRepo(Protocol):
    def list(self) -> list[User]:
        """Return the list of all users."""
        ...
