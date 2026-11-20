from psycopg.errors import IntegrityError, RaiseException

from database.connection import get_db
from utils.exceptions import AppError

def new_message(
    chat_id: str,
    from_uid: str,
    message: str
) -> dict:
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chat (
                    id,
                    from_user_id,
                    message
                )
                VALUES (
                    %s, %s, %s
                )
                RETURNING * 
                """,
                (chat_id,
                 from_uid,
                 message,
                ),
            )
            
            new_mes = cursor.fetchone()
        
        db.commit()
        return new_mes
    
    except IntegrityError as e:
        db.rollback()

        constraint = e.diag.constraint_name

        # from_user_id n'existe pas
        if constraint == "fk_chat_id":
            raise AppError(
                code="CHAT_ID_NOT_FOUND",
                message="The chat does not exist",
                status_code=404,
            )

        # IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The interaction could not be created",
            status_code=409,
        )
    
    except RaiseException as e:
        db.rollback()

        if e.diag.constraint_name == "fk_chat_from_user":
            raise AppError(
                code="CHAT_USER_NOT_IN_MATCH",
                message="The user does not belong to this match",
                status_code=403,
            )

        raise AppError(
            code="DATABASE_ERROR",
            message="A database error occurred",
            status_code=500,
        )

    except Exception:
        db.rollback()
        raise

def get_chat(
    chat_id: str
) -> dict:
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM chat
                WHERE id = %s
                """,
                (chat_id, )
            )
            
            messages = cursor.fetchall()
            
            return messages
    except Exception:
        raise

def send_notif():
    return

def update_read_state():
    return