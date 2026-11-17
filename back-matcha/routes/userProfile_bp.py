from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success, error
import services.userProfile_service as s
from services.messages_service import send_private_message
from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

userProfile_bp = Blueprint("userProfile", __name__, url_prefix="/api/userprofile")

GENDERS = {"Male", "Female", "Other"}

def validate_profile_fields(data):
    if not isinstance(data, dict):
        raise ValidationError("JSON body required")

    result = {}
    required = [
        "age", "gender", "gender_pref", "bio",
        "picture_profile_index", "localisation", "tags",
    ]
    for field in required:
        if field not in data:
            raise ValidationError(f"The field '{field}' is required")
    if data["gender"] not in GENDERS:
        raise ValidationError("gender must be Male, Female or Other")
    result["gender"] = data["gender"]

    pref = data["gender_pref"]
    if not isinstance(pref, list) or not pref or any(p not in GENDERS for p in pref):
        raise ValidationError("gender_pref must be a non-empty list of genders")
    result["gender_pref"] = pref

    bio = data["bio"]
    if not isinstance(bio, str) or not bio.strip() or len(bio) > 2000:
        raise ValidationError("bio must be a non-empty string of 2000 characters or less")
    result["bio"] = bio.strip()

    index = data["picture_profile_index"]
    if isinstance(index, bool) or not isinstance(index, int) or index < 0:
        raise ValidationError("picture_profile_index must be a positive integer")
    result["picture_profile_index"] = index

    return result


@userProfile_bp.route("/", methods=["POST"])
def create_user_profile():
    user_id = (get_jwt_identity(), "user_id")
    data = request.get_json(silent=True)
    fields = validate_profile_fields(data)
    result = s.create_user_profile(fields, user_id)
    return success(result, 201)


@userProfile_bp.route("/<uuid:user_id>/", methods=["GET"])
def get_user_profile_by_id(user_id):
    
    user_id = validate_uuid(user_id, "user_id")
    
    userProfile = s.get_user_profile_by_id_with_pictures(user_id)
    
    
    # send_private_message(
    # socketio,
    # recipient_id=42,
    # message={
    #     "id": 123,
    #     "conversation_id": 10,
    #     "sender_id": 7,
    #     "text": "Bonjour !",
    # })
    
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



