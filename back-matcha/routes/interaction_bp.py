from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid, validate_enum
from utils.response import success
import services.interaction_service as s

interaction_bp = Blueprint("interaction", __name__, url_prefix="/api/interaction")

TYPEOF_INTER = ['Liked', 'Viewed', 'Matched']

@interaction_bp.route("/", methods=["POST"])
def create_interaction():
    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")
    if "from_user_id" not in data:
        raise ValidationError("from_user_id is required")
    if "to_user_id" not in data:
        raise ValidationError("to_user_id is required")
    if "which_interaction" not in data:
        raise ValidationError("which_interaction is required")

    from_user_id = validate_uuid(
        data["from_user_id"],
        "from_user_id"
    )

    to_user_id = validate_uuid(
        data["to_user_id"],
        "to_user_id"
    )

    which_interaction = validate_enum(
        data["which_interaction"],
        "which_interaction",
        TYPEOF_INTER
    )

    result = s.create_interaction(from_user_id, to_user_id, which_interaction)

    return success(result, 201)


@interaction_bp.route("/from/<uuid:user_id>/", methods=["GET"])
def get_all_interaction_from_user_id(user_id):

    user_id = validate_uuid(user_id, "user_id")

    limit = request.args.get("limit", default=20, type=int)
    cursor = request.args.get("cursor")

    interactions_list, next_cursor = s.get_all_interaction_from(
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