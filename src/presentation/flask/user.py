import json
import os

from flask import Blueprint, Response, request

from src.application.requests.user import build_user_list_request
from src.application.responses import ResponseTypes
from src.application.serializers.user import UserJsonEncoder
from src.application.services.user import user_list
from src.infrastructure.repositories.postgresrepo import PostgresRepo

blueprint = Blueprint("user", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

POSTGRES_CONFIG = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_HOSTNAME": os.environ["POSTGRES_HOSTNAME"],
    "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
    "APPLICATION_DB": os.environ["APPLICATION_DB"],
}

@blueprint.route("/users", methods=["GET"])
def users() -> Response:
    qrystr_params: dict[str, dict[str, str]] = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_user_list_request(filters=qrystr_params["filters"])

    repo = PostgresRepo(POSTGRES_CONFIG)
    response = user_list(repo, request_object)

    return Response(
        json.dumps(response.value, cls=UserJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )
