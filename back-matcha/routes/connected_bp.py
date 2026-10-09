from flask import Blueprint, request
import services.authenticate_service as s
from utils.exceptions import ValidationError
from utils.response import success
from flask_jwt_extended import jwt_required, get_jwt_identity

connected_bp = Blueprint(
    "connected",
    __name__,
    url_prefix="/api/connected"
)

@connected_bp.route("/", methods=["GET"])
@jwt_required()
def connected():
    user_id = get_jwt_identity()
    user = s.get_user_by_id(user_id)

    if not user:
        raise ValidationError("User not found")

    return success({
        "message": "Token valide",
        "user_id": user_id
    })