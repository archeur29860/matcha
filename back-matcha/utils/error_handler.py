
from werkzeug.exceptions import HTTPException

from utils.exceptions import AppError
from utils.response import error


def register_error_handlers(app):

    # Erreurs applicatives personnalisées
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return error(
            e.code,
            e.message,
            e.status_code,
            e.details
        )

    # Erreurs HTTP (400, 401, 403, 404, 405, etc.)
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return error(
            e.name.upper().replace(" ", "_"),
            e.description,
            e.code or 500,
            None
        )

    # Erreurs internes inattendues (500)
    @app.errorhandler(Exception)
    def handle_unknown_error(e):

        app.logger.exception("Unhandled exception")

        return error(
            "INTERNAL_ERROR",
            "An internal error occurred",
            500,
            None
        )
