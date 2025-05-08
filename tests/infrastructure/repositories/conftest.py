import pymongo
import pytest
import sqlalchemy

from src.infrastructure.repositories.postgres_objects import Base, UserRelation

USERS = [
    {
        "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "name": "User 1",
        "age": 20,
    },
    {
        "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "name": "User 2",
        "age": 30,
    },
    {
        "id": "913694c6-435a-4366-ba0d-da5334a611b2",
        "name": "User 3",
        "age": 40,
    },
    {
        "id": "eed76e77-55c1-41ce-985d-ca49bf6c0585",
        "name": "User 4",
        "age": 50,
    },
]


@pytest.fixture(scope="session")
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration["POSTGRES_USER"],
        app_configuration["POSTGRES_PASSWORD"],
        app_configuration["POSTGRES_HOSTNAME"],
        app_configuration["POSTGRES_PORT"],
        app_configuration["APPLICATION_DB"],
    )
    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    Base.metadata.create_all(engine)

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def pg_test_data():
    return USERS


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_test_data):
    for u in pg_test_data:
        new_user = UserRelation(
            id=u["id"],
            name=u["name"],
            age=u["age"],
        )
        pg_session_empty.add(new_user)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(UserRelation).delete()


@pytest.fixture(scope="session")
def mg_database_empty(app_configuration):
    client = pymongo.MongoClient(
        host=app_configuration["MONGODB_HOSTNAME"],
        port=int(app_configuration["MONGODB_PORT"]),
        username=app_configuration["MONGODB_USER"],
        password=app_configuration["MONGODB_PASSWORD"],
        authSource="admin",
    )
    db = client[app_configuration["APPLICATION_DB"]]

    yield db

    client.drop_database(app_configuration["APPLICATION_DB"])
    client.close()


@pytest.fixture(scope="function")
def mg_test_data():
    return USERS


@pytest.fixture(scope="function")
def mg_database(mg_database_empty, mg_test_data):
    collection = mg_database_empty.users

    collection.insert_many(mg_test_data)

    yield mg_database_empty

    collection.delete_many({})
