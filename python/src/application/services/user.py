from src.application.entities.user import User
from src.application.interfaces.user_repo import UserRepo


def user_list(repo: UserRepo) -> list[User]:
    return repo.list()
