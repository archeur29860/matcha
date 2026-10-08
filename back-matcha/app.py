import os
<<<<<<< HEAD
from database import db
from utils.error_handler import register_error_handlers
from flask_jwt_extended import JWTManager

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
=======
>>>>>>> master

from flask import Flask
from flask_cors import CORS

from utils.error_handler import register_error_handlers
from database.connection import close_db

from routes.tags_bp import tags_bp
from routes.blocked_bp import blocked_bp
from routes.users_bp import users_bp
from routes.interaction_bp import interaction_bp
from routes.authenticate_bp import auth_bp


app = Flask(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CORS(
    app,
    origins=["http://localhost:5174"],
)


app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)
# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

app.teardown_appcontext(close_db)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------

app.register_blueprint(tags_bp)
app.register_blueprint(blocked_bp)
app.register_blueprint(users_bp)
app.register_blueprint(interaction_bp)
app.register_blueprint(auth_bp)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

register_error_handlers(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.route("/api/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Development server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )