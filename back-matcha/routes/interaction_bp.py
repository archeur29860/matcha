from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid, validate_enum
from utils.response import success
import services.interaction_service as s
import services.match_service as sm
from utils.decorators import profile_completed

interaction_bp = Blueprint("interaction", __name__, url_prefix="/api/interaction")

TYPEOF_INTER = ['Liked', 'Unliked', 'Viewed', 'Blocked', 'Reported']

@interaction_bp.route("/", methods=["POST"])
# @profile_completed
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

    if from_user_id == to_user_id:
        raise ValidationError("Are you that lonely ? user ids must be distinct")

    which_interaction = validate_enum(
        data["which_interaction"],
        "which_interaction",
        TYPEOF_INTER
    )

    if which_interaction not in TYPEOF_INTER:
        raise ValidationError("Must be a valid type of interaction")

    result_inter = s.create_interaction(from_user_id, to_user_id, which_interaction)
    result_match = None
    match_created = False
    match_deleted = False

    # if which_interaction=="Liked" and s.check_like_between(to_user_id, from_user_id):
    #     result_match = sm.create_match(from_user_id, to_user_id)
    #     match_created = True

    # elif which_interaction=="Unlike" and sm.check_match_between(to_user_id, from_user_id):
    #     result_match = sm.delete_match(from_user_id, to_user_id)
    #     match_deleted = True


    return success({
        "interaction": result_inter,
        "match": result_match,
        "match_created": match_created,
        "match_deleted": match_deleted
    }, 201)


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
    typeof_inter = request.args.get("typeof_inter")

    interactions_list, next_cursor = s.get_all_interaction_to(
        user_id,
        limit,
        cursor,
        typeof_inter
        )

    return success({
        "items": interactions_list,
        "pagination": {
            "next_cursor": next_cursor,
            "has_more": next_cursor is not None
        } 
    })

@interaction_bp.route("/<uuid:from_user_id>/<uuid:to_user_id>/", methods=["GET"])
def isLiked(from_user_id, to_user_id):
    
    from_user_id = validate_uuid(from_user_id, "from_user_id")
    to_user_id = validate_uuid(to_user_id, "to_user_id")
    
    isliked = s.check_like_between(from_user_id, to_user_id)
    
    return success(isLiked)