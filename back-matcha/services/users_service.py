from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError
from werkzeug.security import generate_password_hash


def add_user(dict_info: dict) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    username,
                    last_name,
                    first_name,
                    password
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING
                    id,
                    email
                """,
                (
                    dict_info["email"],
                    dict_info["username"],
                    dict_info["last_name"],
                    dict_info["first_name"],
                    generate_password_hash(dict_info["password"]),
                ),
            )

            user = cursor.fetchone()

        db.commit()

        return user

    except IntegrityError:
        db.rollback()

        raise AppError(
            code="USER_ALREADY_EXISTS",
            message="User already exists",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise


def modify_user(dict_info: dict) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET
                    email = %s,
                    username = %s,
                    last_name = %s,
                    first_name = %s,
                    password = %s
                WHERE id = %s
                RETURNING
                    id,
                    email
                """,
                (
                    dict_info["email"],
                    dict_info["username"],
                    dict_info["last_name"],
                    dict_info["first_name"],
                    generate_password_hash(dict_info["password"]),
                    dict_info["user_id"],
                ),
            )

            user = cursor.fetchone()

        if user is None:
            db.rollback()

            raise AppError(
                code="USER_DOESNT_EXISTS",
                message="User doesn't exist",
                status_code=404,
            )

        db.commit()

        return user

    except IntegrityError:
        db.rollback()

        raise AppError(
            code="USER_ALREADY_EXISTS",
            message="User already exists",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise