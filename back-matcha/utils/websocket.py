
from flask import request
from flask_socketio import join_room


def register_socket_events(socketio):

    @socketio.on("connect")
    def handle_connect(auth=None):
        # À remplacer par la vérification réelle
        # de la session ou du token de ton application.
        user_id = authenticate_socket_user(auth)

        if user_id is None:
            return False

        join_room(f"user:{user_id}")

    @socketio.on("disconnect")
    def handle_disconnect(reason=None):
        # Socket.IO retire automatiquement le client
        # de ses rooms à la déconnexion.
        pass


def authenticate_socket_user(auth):
    """
    À connecter à ton authentification existante.

    Retourner l'identifiant vérifié de l'utilisateur,
    ou None si l'authentification échoue.
    """
    return None
