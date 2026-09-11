from flask import Flask
from utils.exceptions import AppError
from utils.response import error


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(e):
        return error(
            e.code,
            e.message,
            e.status_code,
            e.details
        )

    @app.errorhandler(Exception)
    def handle_unknown_error(e):

        app.logger.exception(
            "Unhandled exception"
        )

        return error(
            "INTERNAL_ERROR",
            "An internal error occurred",
            500
        )