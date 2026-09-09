from database import db

class Tags(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(25), unique=True, nullable=False)