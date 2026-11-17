from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError

def create_match(user_id_one, user_id_two):
    h_user, l_user = define_high_low_user_id(user_id_one, user_id_two)
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO matches (
                    user_low_id,
                    user_high_id,
                )
                VALUES (
                    %s,
                    %s
                )
                RETURNING *
                """,
                (
                    l_user,
                    h_user,
                ),
            )

            new_match = cursor.fetchone()

        db.commit()

        return new_match

    except IntegrityError as e:
        db.rollback()

        constraint = e.diag.constraint_name

        # low user id n'existe pas
        if constraint == "fk_low_user":
            raise AppError(
                code="LOW_USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404,
            )

        # high user id n'existe pas
        if constraint == "fk_high_user":
            raise AppError(
                code="HIGH_USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404,
            )
        
        # match non unique
        if constraint == "unique_match_relation":
            raise AppError(
                code="NOT_UNIQUE_MATCH",
                message="Match already exist",
                status_code=409,
            )

        # IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The match could not be created",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise

def delete_match(user_id_one, user_id_two):
    h_user, l_user = define_high_low_user_id(user_id_one, user_id_two)
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM matches
                WHERE user_low_id = %s
                  AND user_high_id = %s
                RETURNING *
                """,
                (
                    l_user,
                    h_user,
                ),
            )

            deleted_match = cursor.fetchone()

        db.commit()

        if deleted_match is None:
            raise AppError(
                code="MATCH_NOT_FOUND",
                message="The match does not exist",
                status_code=404,
            )

        return deleted_match

    except AppError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise

def define_high_low_user_id(user_id_one, user_id_two):
    '''Retourne l'id HIGH puis LOW (HIGH id > LOW id)
    pour l'instanciation de la table de matches.
    '''
    if user_id_one > user_id_two:
        return user_id_one, user_id_two
    return user_id_two, user_id_one