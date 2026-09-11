from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

from utils.exceptions import AppError
import traceback

def insert_relation(user_id, user_id_blocked):

    try:
        result = db.session.execute(
            text("""
                INSERT INTO blocked (user_id, user_id_blocked)
                VALUES (:user_id, :user_id_blocked)
                RETURNING user_id, user_id_blocked
                """),
            {"user_id": user_id,
            "user_id_blocked": user_id_blocked
            })

        relation = result.mappings().one()
        db.session.commit()
        return dict(relation)

    except IntegrityError:
        db.session.rollback()

        raise AppError(
            code="BLOCK_ALREADY_EXISTS",
            message="This block relation already exists",
            status_code=409
        )

    except Exception:
        db.session.rollback()
        raise

def delete_relation(user_id, user_id_blocked):
    try:
        result = db.session.execute(
            text("""
                DELETE FROM blocked
                WHERE user_id = :user_id
                AND user_id_blocked = :user_id_blocked
                RETURNING user_id, user_id_blocked
            """),
            {
                "user_id": user_id,
                "user_id_blocked": user_id_blocked
            }
        )

        relation = result.mappings().first()

        if relation is None:
            db.session.rollback()
            return None

        db.session.commit()

        return dict(relation)
    
    except IntegrityError:
        db.session.rollback()

        raise AppError(
            code="BLOCK_ALREADY_EXISTS",
            message="This block relation already exists",
            status_code=409
        )

    except Exception:
        db.session.rollback()
        raise  