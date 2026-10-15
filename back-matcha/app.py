
import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

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

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5174",
)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-me",
)

CORS(
    app,
    origins=[FRONTEND_ORIGIN],
)

# ---------------------------------------------------------------------------
# Socket.IO
# ---------------------------------------------------------------------------

socketio = SocketIO(
    app,
    cors_allowed_origins=[FRONTEND_ORIGIN],
    async_mode="threading",
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

# Ajouter ici le futur blueprint de messagerie :
# from routes.messages_bp import messages_bp
# app.register_blueprint(messages_bp)

# ---------------------------------------------------------------------------
# Socket events
# ---------------------------------------------------------------------------

from sockets.events import register_socket_events

register_socket_events(socketio)

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
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
