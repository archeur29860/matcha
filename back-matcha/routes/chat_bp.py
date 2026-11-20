from flask import Blueprint, request
from utils.exceptions import ValidationError
from utils.validate import validate_uuid
from utils.response import success
import services.chat_service as s

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@chat_bp.route("/<uuid:chat_id>/", methods=["GET"])
def get_chat(chat_id):

    chat_id = validate_uuid(
        chat_id,
        "chat_id"
    )
    
    chat_result = s.get_chat(chat_id)
    
    return success(chat_result, 200)

@chat_bp.route("/send/<uuid:chat_id>/", methods=["POST"])
def send_message(chat_id):
    
    chat_id = validate_uuid(
        chat_id,
        "chat_id"
    )
    
    data = request.get_json()
    
    if not data:
        raise ValidationError("JSON body required")
    if "from_user_id" not in data:
        raise ValidationError("from_user_id is required")
    if "message" not in data:
        raise ValidationError("message is required")
    
    from_user_id = validate_uuid(
        data["from_user_id"],
        "user_id"
    )
    
    message = data["message"].strip()
    
    result = s.new_message(chat_id, from_user_id, message)
    
    #send notif on socket here
    s.send_notif()
    
    return success(result, 201)
    