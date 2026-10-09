from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success
import services.userProfile_service as s

userProfile_bp = Blueprint("userProfile", __name__, url_prefix="/api/userprofile")

@userProfile_bp.route("/<uuid:user_id>/", methods=["GET"])
def get_user_profile_by_id(user_id):
    
    user_id = validate_uuid(user_id, "user_id")
    
    userProfile = s.get_user_profile_by_id_with_pictures(user_id)
    
    return success(userProfile)