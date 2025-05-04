import json
from unittest import mock

import pytest

from src.application.entities.user import User
from src.application.responses import ResponseFailure, ResponseSuccess, ResponseTypes

data = {
    "id": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "name": "username",
    "age": 20,
}
users = [User.from_dict(data)]


@mock.patch("src.presentation.flask.user.user_list")
def test_get(user_list_mock, http_client):
    user_list_mock.return_value = ResponseSuccess(users)

    http_response = http_client.get("/users")

    user_list_mock.assert_called()
    args, _ = user_list_mock.call_args
    assert args[1].filters == {}

    assert json.loads(http_response.data.decode("UTF-8")) == [data]
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@mock.patch("src.presentation.flask.user.user_list")
def test_get_with_filters(user_list_mock, http_client):
    user_list_mock.return_value = ResponseSuccess(users)

    http_response = http_client.get("/users?filter_age__gt=2&filter_age__lt=6")

    user_list_mock.assert_called()
    args, _ = user_list_mock.call_args
    assert args[1].filters == {"age__gt": "2", "age__lt": "6"}

    assert json.loads(http_response.data.decode("UTF-8")) == [data]
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@pytest.mark.parametrize(
    "response_type, expected_status_code",
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ],
)
@mock.patch("src.presentation.flask.user.user_list")
def test_get_response_failures(
    user_list_mock,
    http_client,
    response_type,
    expected_status_code,
):
    user_list_mock.return_value = ResponseFailure(
        response_type,
        message="Just an error message",
    )

    http_response = http_client.get("/users?dummy_request_string")

    user_list_mock.assert_called()
    assert http_response.status_code == expected_status_code
