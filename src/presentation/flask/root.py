
import json

from flask import Blueprint, Response, url_for

blueprint = Blueprint("root", __name__)

@blueprint.route("/", methods=["GET"])
def root() -> Response:
    endpoints = {
        "docs": url_for("root.docs", _external=True),
    }
    return Response(
        json.dumps(endpoints),
        mimetype="application/json",
        status=200,
    )


@blueprint.route("/docs", methods=["GET"])
def docs() -> Response:
    docs = {
        "endpoints": {
            "users": {
            "url": "http://127.0.0.1:5000/users",
            "description": "Return the list of all users",
            "query_parameters": [
                {
                "filter_age__lt": "Filter users with age less than 30",
                "example_url": "http://127.0.0.1:5000/users?filter_age__lt=30"
                },
                {
                "filter_age__eq": "Filter users with age equal to 30",
                "example_url": "http://127.0.0.1:5000/users?filter_age__eq=30"
                },
                {
                "filter_age__gt": "Filter users with age greater than 30",
                "example_url": "http://127.0.0.1:5000/users?filter_age__gt=30"
                }
            ]
            }
        }
    }
    return Response(
        json.dumps(docs),
        mimetype="application/json",
        status=200,
    )
