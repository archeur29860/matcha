from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_connection = db.Column(db.Date)
    is_online = db.Column(db.Boolean, default=False)
    signaled = db.Column(db.Integer, default=0)