import os
from database import db
from utils.error_handler import register_error_handlers

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from routes.exemple_bp import exemple_bp
from routes.tags_bp import tags_bp
from routes.blocked_bp import blocked_bp
from routes.users_bp import users_bp
from routes.interaction_bp import interaction_bp

app = Flask(__name__)

CORS(app, origins=["http://localhost:5174"])

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)

# Enregistre le groupe de routes
# app.register_blueprint(exemple_bp)
app.register_blueprint(tags_bp)
app.register_blueprint(blocked_bp)
app.register_blueprint(users_bp)
app.register_blueprint(interaction_bp)
register_error_handlers(app)

@app.route("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
