from sqlalchemy import text
from database import db


def get_by_id(id):
    # Bien utiliser des paramètres pour éviter SQL injection
    result = db.session.execute(
        text("SELECT username, email FROM exemple \
        WHERE id=:id"),
        {"id": id}
    )

    exemples = result.fetchall()

    # mapping() -> Transforme la valeur récupérée en clé/valeur par ligne en JSON
    # first()   -> Récupère la première ligne sinon None
    return exemples.mappings().first()
