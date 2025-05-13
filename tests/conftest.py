import pytest

from manage import read_json_configuration
from src.presentation.flask.main import create_app


@pytest.fixture
def flask_app():
    app = create_app("testing")
    return app


@pytest.fixture
def http_client(flask_app):
    return flask_app.test_client()


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true", help="run integration tests")


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue("integration"):
        pytest.skip("need --integration option to run")


@pytest.fixture(scope="session")
def app_configuration():
    return read_json_configuration("testing")
