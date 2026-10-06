from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

from utils.exceptions import AppError, NotFoundError
import traceback


def create_interaction(from_uid, to_uid, typeof_inter):
    try:
        result = db.session.execute(
            text("""
                INSERT INTO interaction
                (from_user_id, to_user_id, which_interaction)
                VALUES (:from_uid, :to_uid, :typeof_inter)
                RETURNING *
            """),
            {
                "from_uid": from_uid,
                "to_uid": to_uid,
                "typeof_inter": typeof_inter,
            }
        )
        new_interaction = result.mappings().one()
        db.session.commit()
        return dict(new_interaction)
    
    except IntegrityError as e:
        db.session.rollback()

        constraint = getattr(e.orig.diag, "constraint_name", None)

        # 1. from_user_id n'existe pas
        if constraint == "fk_from_user":
            raise AppError(
                code="FROM_USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404
            )

        # 2. to_user_id_blocked n'existe pas
        if constraint == "fk_to_user":
            raise AppError(
                code="TO_USER_NOT_FOUND",
                message="The user you are interacting with does not exist",
                status_code=404
            )

        # 3. IntegrityError non prévu
        raise AppError(
            code="INTEGRITY_ERROR",
            message="The block relation could not be created",
            status_code=409
        )

    except Exception:
        db.session.rollback()
        raise


def get_all_interaction_from(user_id, limit=20, cursor=None):

    # Composition de la query
    query = """
        SELECT u.username, i.to_user_id, i.which_interaction, i.created_at
        FROM interaction i
        JOIN users u
        ON i.to_user_id = u.id
        WHERE from_user_id = :user_id
        """

    params = {
        "user_id": user_id,
        "limit": limit + 1
    }

    if cursor:
        query += """
            AND (i.created_at, i.id) < (:created_at, :interaction_id)
            """

        params["created_at"] = cursor["created_at"]
        params["interaction_id"] = cursor["id"]

    query += """
        ORDER BY i.created_at DESC, i.id DESC
        LIMIT :limit
        """

    # Exécution query + error handler (custom Exception)
    try:
        result = db.session.execute(
            text(query),
            params
        )
        interactions = [dict(row) for row in result.mappings().all()]

        if result is None:
            raise NotFoundError

        has_more = len(interactions) > limit

        if has_more:
            interactions = interactions[:limit]

        next_cursor = None

        if has_more:
            last = interactions[-1]

            next_cursor = {
                "created_at": last["created_at"].isoformat(),
                "id": str(last["id"])
            }

        return interactions, next_cursor

    except Exception:
        raise

def get_all_interaction_to(user_id, limit=20, cursor=None):
   # Composition de la query
    query = """
        SELECT u.username, i.from_user_id, i.which_interaction, i.created_at
        FROM interaction i
        JOIN users u
        ON i.from_user_id = u.id
        WHERE to_user_id = :user_id
        """

    params = {
        "user_id": user_id,
        "limit": limit + 1
    }

    if cursor:
        query += """
            AND (i.created_at, i.id) < (:created_at, :interaction_id)
            """

        params["created_at"] = cursor["created_at"]
        params["interaction_id"] = cursor["id"]

    query += """
        ORDER BY i.created_at DESC, i.id DESC
        LIMIT :limit
        """
    # Exécution query + error handler (custom Exception)
    try:
        result = db.session.execute(
            text(query),
            params
        )
        interactions = [dict(row) for row in result.mappings().all()]

        if result is None:
            raise NotFoundError

        has_more = len(interactions) > limit

        if has_more:
            interactions = interactions[:limit]

        next_cursor = None

        if has_more:
            last = interactions[-1]

            next_cursor = {
                "created_at": last["created_at"].isoformat(),
                "id": str(last["id"])
            }

        return interactions, next_cursor

    except Exception:
        raise