from collections.abc import Mapping
from typing import Any


class UserListInvalidRequest:
    def __init__(self) -> None:
        self.errors: list[dict[str, str]] = []

    def add_error(self, parameter: str, message: str) -> None:
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self) -> bool:
        return False


class UserListValidRequest:
    def __init__(self, filters: Mapping[str, Any] | None = None):
        self.filters = filters

    def __bool__(self) -> bool:
        return True


def build_user_list_request(
    filters: Mapping[str, Any] | None = None,
) -> UserListValidRequest | UserListInvalidRequest:
    accepted_filters = ("age__eq", "age__gt", "age__lt")
    invalid_req = UserListInvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error("filters", "Is not iterable")
            return invalid_req

        for key in filters:
            if key not in accepted_filters:
                invalid_req.add_error("filters", f"Key {key} cannot be used")

        if invalid_req.has_errors():
            return invalid_req

    return UserListValidRequest(filters=filters)
