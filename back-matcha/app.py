import os

from flask import Flask
from flask_cors import CORS

from utils.error_handler import register_error_handlers
from database.connection import close_db

from routes.tags_bp import tags_bp
from routes.blocked_bp import blocked_bp
from routes.users_bp import users_bp
from routes.interaction_bp import interaction_bp
from routes.userProfile_bp import userProfile_bp
from routes.pictures_bp import pictures_bp


app = Flask(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CORS(
    app,
    origins=["http://localhost:5174"],
)


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
app.register_blueprint(userProfile_bp)
app.register_blueprint(pictures_bp)


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