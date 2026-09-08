from Flask import Blueprint
from models.exemple_model import Exemple

# Définition d'un Blueprint (bp), pour faire des groupes de routes Flask
exemple_bp = Blueprint("exemple", __name__, url_prefix="/api/exemple")

# app.route -> rattache directement à app
# bp.route  -> permet de grouper les routes et de faciliter 
#              la lisibilité et maintenance du code


# URL et méthode de requête
@exemple_bp.route("/", methods=["POST"])
def create_exemple():
    # Récupération des données jointes
    data = request.get_json()

    # Données json utilisée comme un dict
    if not data:
        return {"error": "JSON body required"}, 400

    if "username" not in data:
        return {"error": "username is required"}, 400

    if "email" not in data:
        return {"error": "email is required"}, 400

    username = data["username"]
    email = data["email"]

    # INSERER LOGIQUE POSTGRE

    # Le json de retour avec code erreur
    return {
        "username": username,
        "email": email
    }, 201

from services.exemple_service import get_by_id

@exemple_bp.route("/<uuid:exemple_id>", methods=["GET"])
def get_by_id_exemple(exemple_id):
    exemple = get_by_id(exemple_id)

    if exemple is None:
        return {"error", "Exemple not found"}, 404
    return exemple, 200

# Exemples d'utilisation
# @exemple_bp.route("/", methods=["GET"])
# @exemple_bp.route("/<int:user_id>", methods=["GET"])

# ----- CODES ERREURS -----
# 200 → OK
# 201 → Created
# 400 → Bad Request
# 401 → Unauthorized
# 403 → Forbidden
# 404 → Not Found
# 500 → Internal Server Error

# ----- EXTRAIRE DATA -----
#json -> request.get_json()
#form -> request.form
#file -> request.files
#body brut -> request.data

