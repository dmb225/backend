import pytest

from src.presentation.flask.app import create_app


@pytest.fixture
def flask_app():
    app = create_app("testing")
    return app


@pytest.fixture
def http_client(flask_app):
    return flask_app.test_client()
