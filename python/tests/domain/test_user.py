import uuid

from src.domain.user import User


def test_user_model_from_dict():
    id = uuid.uuid4()
    init_dict = {
        "id": id,
        "name": "name",
        "age": 33,
    }
    user = User.from_dict(init_dict)

    assert user.id == id
    assert user.name == "name"
    assert user.age == 33


def test_user_model_to_dict():
    init_dict = {
        "id": uuid.uuid4(),
        "name": "name",
        "age": 33,
    }

    user = User.from_dict(init_dict)
    assert user.to_dict() == init_dict


def test_user_model_comparison():
    init_dict = {
        "id": uuid.uuid4(),
        "name": "name",
        "age": 33,
    }

    user1 = User.from_dict(init_dict)
    user2 = User.from_dict(init_dict)

    assert user1 == user2
