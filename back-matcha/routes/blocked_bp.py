from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success
import services.blocked_service as s

blocked_bp = Blueprint("blocked", __name__, url_prefix="/api/blocked")


@blocked_bp.route("/", methods=["POST"])
def block_a_profil():
    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")
    if "user_id" not in data:
        raise ValidationError("user_id is required")
    if "user_id_blocked" not in data:
        raise ValidationError("user_id_blocked is required")

    user_id = validate_uuid(
        data["user_id"],
        "user_id"
    )
    
    user_id_blocked = validate_uuid(
        data["user_id_blocked"],
        "user_id_blocked"
    )
    result = s.insert_relation(user_id, user_id_blocked)
    
    if result is None:
        return success(status=204)

    return success(result, 201)


@blocked_bp.route("/", methods=["DELETE"])
def unblock_a_profile():

    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")
    if "user_id" not in data:
        raise ValidationError("user_id is required")
    if "user_id_blocked" not in data:
        raise ValidationError("user_id_blocked is required")

    user_id = validate_uuid(
        data["user_id"],
        "user_id"
    )
    
    user_id_blocked = validate_uuid(
        data["user_id_blocked"],
        "user_id_blocked"
    )

    result = s.delete_relation(
        user_id,
        user_id_blocked
    )

    return success(result, 200)

@blocked_bp.route("/<uuid:user_id>", methods=["GET"])
def get_all_blocked_user(user_id):
    blocked_list = s.
