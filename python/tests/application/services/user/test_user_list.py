import uuid
from unittest import mock

import pytest

from src.application.entities.user import User
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


def test_room_list_without_parameters(users):
    repo = mock.Mock()
    repo.list.return_value = users

    result = user_list(repo)

    repo.list.assert_called_with()
    assert result == users
