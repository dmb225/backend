from src.application.interfaces.user_repo import UserRepo
from src.application.requests.user import UserListInvalidRequest, UserListValidRequest
from src.application.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)


def user_list(
    repo: UserRepo, request: UserListInvalidRequest | UserListValidRequest
) -> ResponseFailure | ResponseSuccess:
    if not request:
        return build_response_from_invalid_request(request)
    try:
        assert isinstance(request, UserListValidRequest)
        users = repo.list(filters=request.filters)
        return ResponseSuccess(users)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
