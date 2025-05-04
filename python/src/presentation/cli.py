from src.application.entities.user import User
from src.application.requests.user import build_user_list_request
from src.application.responses import ResponseSuccess
from src.application.services.user import user_list
from src.infrastructure.repositories.user import UserMem

users = [
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

request = build_user_list_request()
repo = UserMem(users)
response = user_list(repo, request)

assert isinstance(response, ResponseSuccess)
assert isinstance(response.value, list)
for user in response.value:
    assert isinstance(user, User)

print([user.to_dict() for user in response.value])
