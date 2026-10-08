from flask import Blueprint, request
import services.users_service as s
from utils.exceptions import ValidationError
from werkzeug.security import check_password_hash
from utils.response import success

auth_bp = Blueprint(
    "auth", __name__, url_prefix="/api/auth"
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
    
    user = s.authenticate_user(
        data["email"],
        data["password"]
    )

    if check_password_hash(user["password"], data["password"]) is True and data["email"] = :
        access_token = create_access_token(
            identity=str(user.id)
        )
        return success({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        })