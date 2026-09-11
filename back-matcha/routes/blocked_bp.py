from flask import Blueprint, request
from models.tags_m import Tags
import services.blocked_service as s

blocked_bp = Blueprint("blocked", __name__, url_prefix="/api/blocked")


@blocked_bp.route("/", methods=["POST"])
def block_a_profil():
    data = request.get_json()

    if not data:
        return {"error":"JSON body required"}, 400
    
    if "user_id" not in data or "user_id_blocked" not in data:
        return {"error": "users id are mandatory"}, 400

    user_id = data["user_id"]
    user_id_blocked = data["user_id_blocked"]

    result = s.insert_relation(user_id, user_id_blocked)

    if result is None:
        return {"error": "something went wrong"}, 500
    
    return {
        "success": True
    }, 201

@blocked_bp.route("/", methods=["DELETE"])
def unblock_a_profile():

    data = request.get_json()

    if not data:
        return {"error": "JSON body required"}, 400


    if "user_id" not in data or "user_id_blocked" not in data:
        return {"error": "users id are mandatory"}, 400

    result = s.delete_relation(
        data["user_id"],
        data["user_id_blocked"]
    )

    if result is None:
        return {"error": "something went wrong"}, 500

    return {
        "success": True
    }, 200