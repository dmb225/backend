import pytest

from src.application.requests.user import (
    UserListValidRequest,
    build_user_list_request,
)


def test_build_user_list_request_without_parameters():
    request: UserListValidRequest = build_user_list_request()

    assert request.filters is None
    assert bool(request) is True


def test_build_user_list_request_from_empty_dict():
    request: UserListValidRequest = build_user_list_request({})

    assert request.filters == {}
    assert bool(request) is True


def test_build_user_list_request_with_invalid_filters_parameter():
    request = build_user_list_request(filters=5)

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


def test_build_user_list_request_with_incorrect_filter_keys():
    request = build_user_list_request(filters={"a": 1})

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


@pytest.mark.parametrize("key", ["age__eq", "age__gt", "age__lt"])
def test_build_user_list_request_accepted_filters(key):
    filters = {key: 1}

    request = build_user_list_request(filters=filters)

    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["name__gt", "name__lt"])
def test_build_user_list_request_rejected_filters(key):
    filters = {key: 1}

    request = build_user_list_request(filters=filters)

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False
