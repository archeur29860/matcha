class AppError(Exception):
    def __init__(self, code, message, status_code=400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

        super().__init__(message)

class ValidationError(AppError):
    def __init__(self, message, details=None):
        super().__init__(
            "VALIDATION_ERROR",
            message,
            400,
            details
        )

class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(
            "NOT_FOUND",
            message,
            404
        )


class ConflictError(AppError):
    def __init__(self, message):
        super().__init__(
            "CONFLICT",
            message,
            409
        )

# | HTTP  | Code API           | Utilisation                      |
# | ----- | ------------------ | -------------------------------- |
# | `200` | —                  | GET / modification réussie       |
# | `201` | —                  | Création réussie                 |
# | `204` | —                  | Suppression sans contenu         |
# | `400` | `VALIDATION_ERROR` | Données invalides                |
# | `401` | `UNAUTHORIZED`     | Non connecté                     |
# | `403` | `FORBIDDEN`        | Pas les permissions              |
# | `404` | `NOT_FOUND`        | Ressource inexistante            |
# | `409` | `CONFLICT`         | Conflit / doublon                |
# | `422` | `INVALID_DATA`     | Données sémantiquement invalides |
# | `500` | `INTERNAL_ERROR`   | Erreur serveur                   |
