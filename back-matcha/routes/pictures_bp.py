from pathlib import Path
from flask import Blueprint, send_from_directory

pictures_bp = Blueprint("pictures", __name__)

# Si le dossier pictures se trouve dans /app/pictures
PICTURES_DIR = Path(__file__).resolve().parent.parent / "pictures"

@pictures_bp.route("/api/pictures/<path:filename>")
def get_picture(filename):
    return send_from_directory(PICTURES_DIR, filename)