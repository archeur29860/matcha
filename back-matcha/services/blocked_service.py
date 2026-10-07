from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

from utils.exceptions import AppError, NotFoundError
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

    except IntegrityError as e:
        db.session.rollback()

        constraint = getattr(e.orig.diag, "constraint_name", None)

        # 1. Relation déjà existante
        if constraint == "unique_block_relation":
            raise AppError(
                code="BLOCK_ALREADY_EXISTS",
                message="This block relation already exists",
                status_code=409
            )

        # 2. user_id n'existe pas
        if constraint == "fk_user":
            raise AppError(
                code="USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404
            )

        # 3. user_id_blocked n'existe pas
        if constraint == "fk_user_blocked":
            raise AppError(
                code="BLOCKED_USER_NOT_FOUND",
                message="The user you are trying to block does not exist",
                status_code=404
            )

        # 4. IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The block relation could not be created",
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

def get_all_blocked_user(user_id):
    try:
        result = db.session.execute(
            text("""
            SELECT u.id, u.username, u.last_name, u.first_name
            FROM blocked b
            JOIN users u
            ON b.user_id_blocked = u.id
            WHERE b.user_id = :user_id
            """),
            {
                "user_id" : user_id
            }
        )

        relations = result.mappings().all()

        if relations is None:
            db.session.rollback()
            raise NotFoundError

        return [
            {
                "username": row["username"],
                "last_name": row["last_name"],
                "first_name": row["first_name"]
            }
            for row in relations
        ]

    except Exception:
        raise