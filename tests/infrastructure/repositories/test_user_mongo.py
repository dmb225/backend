from uuid import UUID

import pytest

from src.infrastructure.repositories import mongorepo

pytestmark = pytest.mark.integration


def test_repository_list_without_parameters(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get()

    assert len(repo_users) == 4
    assert set([r.id for r in repo_users]) == set([UUID(r["id"]) for r in mg_test_data])


def test_repository_list_with_age_equal_filter(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get(filters={"age__eq": 30})

    assert len(repo_users) == 1
    assert repo_users[0].id == UUID("fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a")


def test_repository_list_with_age_less_than_filter(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get(filters={"age__lt": 40})

    assert len(repo_users) == 2
    assert set([r.id for r in repo_users]) == {
        UUID("f853578c-fc0f-4e65-81b8-566c5dffa35a"),
        UUID("fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a"),
    }


def test_repository_list_with_age_greater_than_filter(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get(filters={"age__gt": 30})

    assert len(repo_users) == 2
    assert set([r.id for r in repo_users]) == {
        UUID("913694c6-435a-4366-ba0d-da5334a611b2"),
        UUID("eed76e77-55c1-41ce-985d-ca49bf6c0585"),
    }


def test_repository_list_with_age_between_filter(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get(filters={"age__lt": 45, "age__gt": 35})

    assert len(repo_users) == 1
    assert repo_users[0].id == UUID("913694c6-435a-4366-ba0d-da5334a611b2")


def test_repository_list_with_age_as_string(app_configuration, mg_database, mg_test_data):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get(filters={"age__lt": "40"})

    assert len(repo_users) == 2
    assert set([r.id for r in repo_users]) == {
        UUID("f853578c-fc0f-4e65-81b8-566c5dffa35a"),
        UUID("fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a"),
    }
