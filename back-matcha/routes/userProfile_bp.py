from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success, error
import services.userProfile_service as s
from services.messages_service import send_private_messend_private_message

userProfile_bp = Blueprint("userProfile", __name__, url_prefix="/api/userprofile")

@userProfile_bp.route("/<uuid:user_id>/", methods=["GET"])
def get_user_profile_by_id(user_id):
    
    user_id = validate_uuid(user_id, "user_id")
    
    userProfile = s.get_user_profile_by_id_with_pictures(user_id)
    
    
    send_private_message(
    socketio,
    recipient_id=42,
    message={
        "id": 123,
        "conversation_id": 10,
        "sender_id": 7,
        "text": "Bonjour !",
    })
    
    return success(userProfile)


@userProfile_bp.route("/list/<uuid:user_id>/", methods=["GET"])
def get_list_profile_for_user_id(user_id):
    user_id = validate_uuid(user_id, "user_id")
    
    limit = request.args.get("limit", default=20, type=int)
    cursor = request.args.get("cursor", default=None, type=str)

    if cursor:
        cursor = validate_uuid(cursor, "cursor")
    limit = max(1, min(limit, 50))


    result = s.get_list_profile_by_id(
        user_id,
        limit=limit,
        cursor=cursor,
    )

    return success(result)