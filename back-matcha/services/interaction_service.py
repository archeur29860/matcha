from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError


def create_interaction(
    from_uid: int,
    to_uid: int,
    typeof_inter: str,
) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO interactions (
                    from_user_id,
                    to_user_id,
                    which_interaction
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                RETURNING *
                """,
                (
                    from_uid,
                    to_uid,
                    typeof_inter,
                ),
            )

            new_interaction = cursor.fetchone()

        db.commit()

        return new_interaction

    except IntegrityError as e:
        db.rollback()

        constraint = e.diag.constraint_name

        # from_user_id n'existe pas
        if constraint == "fk_from_user":
            raise AppError(
                code="FROM_USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404,
            )

        # to_user_id n'existe pas
        if constraint == "fk_to_user":
            raise AppError(
                code="TO_USER_NOT_FOUND",
                message="The user you are interacting with does not exist",
                status_code=404,
            )

        # IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The interaction could not be created",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise


def get_all_interaction_from(
    user_id: int,
    limit: int = 20,
    cursor: dict | None = None,
) -> tuple[list[dict], dict | None]:
    db = get_db()

    query = """
        SELECT
            u.username,
            i.to_user_id,
            i.which_interaction,
            i.created_at,
            i.id
        FROM interactions i
        JOIN users u
            ON i.to_user_id = u.id
        WHERE i.from_user_id = %s
    """

    params: list = [user_id]

    if cursor:
        query += """
            AND (i.created_at, i.id) < (%s, %s)
        """

        params.extend(
            [
                cursor["created_at"],
                cursor["id"],
            ]
        )

    query += """
        ORDER BY
            i.created_at DESC,
            i.id DESC
        LIMIT %s
    """

    params.append(limit + 1)

    try:
        with db.cursor() as cursor_db:
            cursor_db.execute(
                query,
                tuple(params),
            )

            interactions = cursor_db.fetchall()

        has_more = len(interactions) > limit

        if has_more:
            interactions = interactions[:limit]

        next_cursor = None

        if has_more:
            last = interactions[-1]

            next_cursor = {
                "created_at": last["created_at"].isoformat(),
                "id": str(last["id"]),
            }

        return interactions, next_cursor

    except Exception:
        raise


def get_all_interaction_to(
    user_id: int,
    limit: int = 20,
    cursor: dict | None = None,
) -> tuple[list[dict], dict | None]:
    db = get_db()

    query = """
        SELECT
            u.username,
            i.from_user_id,
            i.which_interaction,
            i.created_at,
            i.id
        FROM interactions i
        JOIN users u
            ON i.from_user_id = u.id
        WHERE i.to_user_id = %s
    """

    params: list = [user_id]

    if cursor:
        query += """
            AND (i.created_at, i.id) < (%s, %s)
        """

        params.extend(
            [
                cursor["created_at"],
                cursor["id"],
            ]
        )

    query += """
        ORDER BY
            i.created_at DESC,
            i.id DESC
        LIMIT %s
    """

    params.append(limit + 1)

    try:
        with db.cursor() as cursor_db:
            cursor_db.execute(
                query,
                tuple(params),
            )

            interactions = cursor_db.fetchall()

        has_more = len(interactions) > limit

        if has_more:
            interactions = interactions[:limit]

        next_cursor = None

        if has_more:
            last = interactions[-1]

            next_cursor = {
                "created_at": last["created_at"].isoformat(),
                "id": str(last["id"]),
            }

        return interactions, next_cursor

    except Exception:
        raise