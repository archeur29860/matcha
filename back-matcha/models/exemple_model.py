from database import db

class Exemple(db.Model):
    # Lie la class à une table existante dans Postgre
    # Sinon la class crée une nouvelle table - à éviter.
    __tablename__ = "exemple"
    
    # Définition des colonnes (reprendre DB)
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)