import pytest

from src.application.entities.user import User
from src.infrastructure.repositories.user import UserMem


@pytest.fixture
def user_dicts():
    return [
        {
            "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "name": "user1",
            "age": 20,
        },
        {
            "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "name": "user2",
            "age": 25,
        },
        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "name": "user3",
            "age": 30,
        },
        {
            "id": "eed76e77-55c1-41ce-985d-ca49bf6c0585",
            "name": "user4",
            "age": 35,
        },
    ]


def test_repository_list_without_parameters(user_dicts):
    repo = UserMem(user_dicts)

    users = [User.from_dict(i) for i in user_dicts]

    assert repo.list() == users
