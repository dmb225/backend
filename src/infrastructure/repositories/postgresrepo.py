from typing import Any, Mapping, Optional, Sequence
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.application.entities.user import User
from src.application.interfaces.user_repo import UserRepo
from src.infrastructure.repositories.postgres_objects import Base, UserRelation


class PostgresRepo(UserRepo):
    def __init__(self, configuration: dict[str, str]) -> None:
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            configuration["POSTGRES_USER"],
            configuration["POSTGRES_PASSWORD"],
            configuration["POSTGRES_HOSTNAME"],
            configuration["POSTGRES_PORT"],
            configuration["APPLICATION_DB"],
        )

        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)

    def get(self, filters: Optional[Mapping[str, Any]] = None) -> list[User]:
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(UserRelation)

        if filters is None:
            return self._create_user_objects(query.all())

        if "age__eq" in filters:
            query = query.filter(UserRelation.age == filters["age__eq"])

        if "age__lt" in filters:
            query = query.filter(UserRelation.age < filters["age__lt"])

        if "age__gt" in filters:
            query = query.filter(UserRelation.age > filters["age__gt"])

        return self._create_user_objects(query.all())

    @staticmethod
    def _create_user_objects(results: Sequence["UserRelation"]) -> list[User]:
        return [
            User(
                id=UUID(q.id),
                name=q.name,
                age=q.age,
            )
            for q in results
        ]
