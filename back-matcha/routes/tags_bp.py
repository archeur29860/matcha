from flask import Blueprint, request
from models.tags_m import Tags
import services.tags_service as s

tags_bp = Blueprint("tags", __name__, url_prefix="/api/tags")

@tags_bp.route("/", methods=["POST"])
def create_tag():
    data = request.get_json()

    if not data:
        return {"error":"JSON body required"}, 400

    if "label" not in data:
        return {"error" : "label is required"}, 400
    
    label = data["label"].strip()

    if not label:
        return {"error": "label cannot be empty"}, 400
    
    if len(label) > 25:
        return {"error": "label must be 25 characters or less"}, 400
    
    result = s.add_tag(label)

    if result is None:
        return {"error": "Tag already exists"}, 409

    return {
        "id": result["id"],
        "label": result["label"]
        }, 201

@tags_bp.route("/", methods=["GET"])
def get_all_tags():
    
    result = s.get_all_tags()

    return [
        {
            "id": tag["id"],
            "label": tag["label"]
        }
        for tag in result
    ], 200