import uuid
from unittest import mock

import pytest

from src.application.entities.user import User
from src.application.requests.user import build_user_list_request
from src.application.responses import ResponseTypes
from src.application.services.user import user_list


@pytest.fixture
def users():
    user_1 = User(id=uuid.uuid4(), name="user1", age=20)

    user_2 = User(
        id=uuid.uuid4(),
        name="user2",
        age=30,
    )

    user_3 = User(
        id=uuid.uuid4(),
        name="user3",
        age=25,
    )

    user_4 = User(
        id=uuid.uuid4(),
        name="user4",
        age=35,
    )

    return [user_1, user_2, user_3, user_4]


def test_user_list_without_parameters(users):
    repo = mock.Mock()
    repo.get.return_value = users

    request = build_user_list_request()
    result = user_list(repo, request)

    repo.get.assert_called_with(filters=None)
    assert result.value == users


def test_user_list_with_filters(users):
    repo = mock.Mock()
    repo.get.return_value = users

    qry_filters = {"age__eq": 5}
    request = build_user_list_request(filters=qry_filters)
    response = user_list(repo, request)

    assert bool(response) is True
    repo.get.assert_called_with(filters=qry_filters)
    assert response.value == users


def test_user_list_handles_generic_error():
    repo = mock.Mock()
    repo.get.side_effect = Exception("Just an error message")

    request = build_user_list_request(filters={})
    response = user_list(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message",
    }


def test_user_list_handles_bad_request():
    repo = mock.Mock()

    request = build_user_list_request(filters=5)
    response = user_list(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
