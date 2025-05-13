import json
import logging
import os

from flask import Blueprint, Response, request

from src.application.interfaces.user_repo import UserRepo
from src.application.requests.user import build_user_list_request
from src.application.responses import ResponseTypes
from src.application.serializers.user import UserJsonEncoder
from src.application.services.user import user_list
from src.infrastructure.repositories.postgresrepo import PostgresRepo
from src.infrastructure.repositories.user_mem import UserMem
from src.presentation.flask.data import DATA

logger = logging.getLogger(__name__)


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


def get_repository() -> UserRepo:
    if os.environ.get("FLASK_CONFIG", "development") == "production":
        return PostgresRepo(POSTGRES_CONFIG)
    return UserMem(DATA)


@blueprint.route("/users", methods=["GET"])
def users() -> Response:
    qrystr_params: dict[str, dict[str, str]] = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_user_list_request(filters=qrystr_params["filters"])

    repo = get_repository()
    response = user_list(repo, request_object)

    return Response(
        json.dumps(response.value, cls=UserJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )
