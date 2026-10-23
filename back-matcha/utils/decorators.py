from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.profile_full_service import profile_is_complete


def profile_completed(function):
    @wraps(function)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()

        if not profile_is_complete(user_id):
            return jsonify({
                "error": "incomplet profile",
                "message": "need to complete your profile."
            }), 403

        return function(*args, **kwargs)

    return wrapper

