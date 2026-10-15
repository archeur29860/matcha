
def notify_user(socketio, user_id, notification):
    socketio.emit(
        "new_notification",
        notification,
        to=f"user:{user_id}",
    )


def send_private_message(
    socketio,
    recipient_id,
    message,
):
    socketio.emit(
        "new_message",
        message,
        to=f"user:{recipient_id}",
    )
