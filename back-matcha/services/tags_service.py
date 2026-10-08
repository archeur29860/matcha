from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import ConflictError


def insert_tag(new_label: str) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tags (
                    label
                )
                VALUES (%s)
                RETURNING
                    id,
                    label
                """,
                (new_label,),
            )

            tag = cursor.fetchone()

        db.commit()

        return tag

    except IntegrityError:
        db.rollback()

        raise ConflictError(
            "Resource already exists"
        )

    except Exception:
        db.rollback()
        raise


def get_all_tags() -> list[dict]:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    label
                FROM tags
                ORDER BY label ASC
                """
            )

            tags = cursor.fetchall()

        return tags

    except Exception:
        db.rollback()
        raise