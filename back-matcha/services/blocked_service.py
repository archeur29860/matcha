from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError, NotFoundError


def insert_relation(
    user_id: str,
    user_id_blocked: str,
) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO blocked (
                    user_id,
                    user_id_blocked
                )
                VALUES (%s, %s)
                RETURNING
                    user_id,
                    user_id_blocked
                """,
                (
                    user_id,
                    user_id_blocked,
                ),
            )

            relation = cursor.fetchone()

        db.commit()

        return relation

    except IntegrityError as e:
        db.rollback()

        constraint = e.diag.constraint_name

        # Relation déjà existante
        if constraint == "unique_block_relation":
            raise AppError(
                code="BLOCK_ALREADY_EXISTS",
                message="This block relation already exists",
                status_code=409,
            )

        # L'utilisateur qui bloque n'existe pas
        if constraint == "fk_user":
            raise AppError(
                code="USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404,
            )

        # L'utilisateur bloqué n'existe pas
        if constraint == "fk_user_blocked":
            raise AppError(
                code="BLOCKED_USER_NOT_FOUND",
                message="The user you are trying to block does not exist",
                status_code=404,
            )

        # IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The block relation could not be created",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise


def delete_relation(
    user_id: str,
    user_id_blocked: str,
) -> dict | None:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM blocked
                WHERE user_id = %s
                AND user_id_blocked = %s
                RETURNING
                    user_id,
                    user_id_blocked
                """,
                (
                    user_id,
                    user_id_blocked,
                ),
            )

            relation = cursor.fetchone()

        # Aucune relation trouvée
        if relation is None:
            db.rollback()
            raise NotFoundError

        db.commit()

        return relation

    except Exception:
        db.rollback()
        raise


def get_all_blocked_user(
    user_id: str,
) -> list[dict]:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    u.id,
                    u.username,
                    u.last_name,
                    u.first_name
                FROM blocked b
                JOIN users u
                    ON b.user_id_blocked = u.id
                WHERE b.user_id = %s
                """,
                (user_id,),
            )

            relations = cursor.fetchall()

        if not relations:
            raise NotFoundError

        return [
            {
                "username": row["username"],
                "last_name": row["last_name"],
                "first_name": row["first_name"],
            }
            for row in relations
        ]

    except Exception:
        raise