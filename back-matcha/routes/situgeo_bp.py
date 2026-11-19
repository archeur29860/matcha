from flask import Blueprint, request
import services.situgeo_service as s
from utils.exceptions import ValidationError
from utils.response import success
from utils.validate import validate_uuid

situgeo_bp = Blueprint("situgeo", __name__, url_prefix="/api/situgeo")

@situgeo_bp.route("/", methods=["POST"])
def create_situgeo():
    data = request.get_json()
    
    if not data:
        raise ValidationError("JSON body required")

    if "user_id" not in data:
        raise ValidationError("user_id is required")
    
    user_id = validate_uuid(
        data["user_id"],
        "user_id"
    )
    
    if "gps_consent" not in data:
        raise ValidationError("gps_consent cannot be empty")

    if not isinstance(data["gps_consent"], bool):
        raise ValidationError("gps_consent must be a boolean")

    gps_consent = data["gps_consent"]

    situgeo = None

    if "lon" in data and "lat" in data:
        lon = float(data["lon"])
        if not lon:
            raise ValidationError("lon cannot be empty")
        
        lat = float(data["lat"])
        if not lat:
            raise ValidationError("lat cannot be empty")
        
        situgeo = s.reverse_geocode(lat, lon)

    elif "label" in data:
        label = data["label"].strip()
        if not label:
            raise ValidationError("label cannot be empty")
        
        situgeo = s.geocode_city(label)

    else:
        raise ValidationError("must contain situgeo information by label or point")
    
    if not situgeo:
        raise ValidationError("situgeo cannot be empty")

    result = s.upsert_user_location(
        user_id=user_id,
        city=situgeo["city"],
        postcode=situgeo["postcode"],
        department=situgeo["department"],
        lat=situgeo["latitude"],
        long=situgeo["longitude"],
        gps_consent=gps_consent,
        street=situgeo["street"],
        district=situgeo["district"]
    )
    
    return success(result, 201)