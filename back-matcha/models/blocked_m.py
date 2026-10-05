from database import db

class Blocked(db.Model):
    __tablename__ = "blocked"

    user_id = db.Column(UUID(as_uuid=True))
    user_id_blocked = db.Column(UUID(as_uuid=True))
