from flask import Blueprint, request
from models.tags_m import Tags
import services.tags_service as s
from utils.exceptions import ValidationError
from utils.response import success

tags_bp = Blueprint("tags", __name__, url_prefix="/api/tags")

@tags_bp.route("/", methods=["POST"])
def create_tag():
    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")

    if "label" not in data:
        raise ValidationError("label is required")
    
    label = data["label"].strip()

    if not label:
        raise ValidationError("label cannot be empty")
    
    if len(label) > 25:
        raise ValidationError("label must be 25 characters or less")
    
    result = s.insert_tag(label)

    return success(result, 201)


@tags_bp.route("/", methods=["GET"])
def get_all_tags():
    
    result = s.get_all_tags()

    return success(result)