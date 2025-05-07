import pytest

from src.application.entities.user import User
from src.infrastructure.repositories.user_mem import UserMem


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

    assert repo.get() == users


def test_repository_list_with_age_equal_filter(user_dicts):
    repo = UserMem(user_dicts)

    users = repo.get(filters={"age__eq": 30})

    assert len(users) == 1
    assert users[0].age == 30


@pytest.mark.parametrize("age", [30, "30"])
def test_repository_list_with_age_less_than_filter(user_dicts, age):
    repo = UserMem(user_dicts)

    users = repo.get(filters={"age__lt": age})

    assert len(users) == 2
    assert set([u.age for u in users]) == {
        20,
        25,
    }


@pytest.mark.parametrize("age", [28, "28"])
def test_repository_list_with_age_greater_than_filter(user_dicts, age):
    repo = UserMem(user_dicts)

    users = repo.get(filters={"age__gt": age})

    assert len(users) == 2
    assert set([u.age for u in users]) == {
        30,
        35,
    }


def test_repository_list_age_between_filter(user_dicts):
    repo = UserMem(user_dicts)

    users = repo.get(filters={"age__lt": 33, "age__gt": 27})

    assert len(users) == 1
    assert users[0].id == "913694c6-435a-4366-ba0d-da5334a611b2"
