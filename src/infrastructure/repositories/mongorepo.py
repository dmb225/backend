from typing import Any, Mapping, Optional
from uuid import UUID

from pymongo.mongo_client import MongoClient
from pymongo.synchronous.cursor import Cursor

from src.application.entities.user import User


class MongoRepo:
    def __init__(self, configuration: dict[str, str]) -> None:
        client: MongoClient[Mapping[str, Any]]  = MongoClient(
            host=configuration["MONGODB_HOSTNAME"],
            port=int(configuration["MONGODB_PORT"]),
            username=configuration["MONGODB_USER"],
            password=configuration["MONGODB_PASSWORD"],
            authSource="admin",
        )

        self.db = client[configuration["APPLICATION_DB"]]

    def get(self, filters: Optional[Mapping[str, Any]] = None) -> list[User]:
        collection = self.db.users

        if filters is None:
            result = collection.find()
        else:
            mongo_filter: dict[str, Any] = {}
            for key, value in filters.items():
                key, operator = key.split("__")

                filter_value = mongo_filter.get(key, {})

                if key == "age":
                    value = int(value)

                filter_value[f"${operator}"] = value
                mongo_filter[key] = filter_value

            result = collection.find(mongo_filter)

        return self._create_user_objects(result)

    @staticmethod
    def _create_user_objects(results: Cursor[Mapping[str, Any]]) -> list[User]:
        return [
            User(
                id=UUID(q["id"]),
                name=q["name"],
                age=q["age"],
            )
            for q in results
        ]
