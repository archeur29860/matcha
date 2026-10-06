from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success
import services.interaction_service as s

interaction_bp = Blueprint("interaction", __name__, url_prefix="/api/interaction")

@interaction_bp.route("/from/<uuid:user_id>/", methods=["GET"])
def get_all_interaction_from_user_id(user_id):

    user_id = validate_uuid(user_id, "user_id")

    limit = request.args.get("limit", default=20, type=int)
    cursor = request.args.get("cursor")

    interactions_list, next_cursor = s.get_all_interaction(
        user_id,
        limit,
        cursor
        )

    return success({
        "items": interactions_list,
        "pagination": {
            "next_cursor": next_cursor,
            "has_more": next_cursor is not None
        } 
    })


@interaction_bp.route("/to/<uuid:user_id>/", methods=["GET"])
def get_all_interaction_to_user_id(user_id):

    user_id = validate_uuid(user_id, "user_id")

    limit = request.args.get("limit", default=20, type=int)
    cursor = request.args.get("cursor")

    interactions_list, next_cursor = s.get_all_interaction_to(
        user_id,
        limit,
        cursor
        )

    return success({
        "items": interactions_list,
        "pagination": {
            "next_cursor": next_cursor,
            "has_more": next_cursor is not None
        } 
    })