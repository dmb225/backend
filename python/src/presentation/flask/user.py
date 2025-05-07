import json

from flask import Blueprint, Response, request

from src.application.requests.user import build_user_list_request
from src.application.responses import ResponseTypes
from src.application.serializers.user import UserJsonEncoder
from src.application.services.user import user_list
from src.infrastructure.repositories.user_mem import UserMem

blueprint = Blueprint("user", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

DATA = [
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


@blueprint.route("/users", methods=["GET"])
def users() -> Response:
    qrystr_params: dict[str, dict[str, str]] = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_user_list_request(filters=qrystr_params["filters"])

    repo = UserMem(DATA)
    response = user_list(repo, request_object)

    return Response(
        json.dumps(response.value, cls=UserJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )
