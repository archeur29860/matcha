from flask import request
from flask_socketio import join_room
from flask_jwt_extended import decode_token

def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect(auth=None):
        # print(f"[SOCKET] Client connecté : {request.sid}")
        if not isinstance(auth, dict):
            return False

        token = auth.get("token")

        if not isinstance(token, str) or not token:
            print("[SOCKET] connexion error: missing token")
            return False

        try:
            payload = decode_token(token)
            user_id = payload.get("sub")

            if user_id is None:
                print("[SOCKET] connexion error: missing user")
                return False

            user_id = str(user_id)

            join_room(f"user:{user_id}")

            print(f"WebSocket connected: user {user_id}")
            return True

        except Exception as exc:
            # if the toke nis  unvalid or refused
            print(f"[SOCKET] connexion error: unvalid token  {type(exc).__name__}")
            return False

    @socketio.on("disconnect")
    def handle_disconnect(reason=None):
        print(f"WebSocket disconnect : {request.sid}, raison={reason}")