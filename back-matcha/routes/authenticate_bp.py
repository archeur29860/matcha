from flask import Blueprint, request
import services.authenticate_service as s
from utils.exceptions import ValidationError
from werkzeug.security import check_password_hash
from utils.response import success
from flask_jwt_extended import create_access_token

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.route("/", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")

    if "email" not in data:
        raise ValidationError("email is required")
    if "password" not in data:
        raise ValidationError("password is required")
    
    user = s.get_authenticate_user(
        data["email"]
    )
    if not user:
        raise ValidationError("Invalid email or password")

    if not check_password_hash(user["password"], data["password"]):
        raise ValidationError("Invalid email or password")
    # if user["password"] != data["password"] :
    #     raise ValidationError("Invalid email or password")

    access_token = create_access_token(
        identity=str(user["id"])
    )
    return success({
        "access_token": access_token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        }
    })