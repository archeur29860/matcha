from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

from utils.exceptions import AppError, NotFoundError
import traceback

def get_all_interaction_from(user_id, limit=20, cursor=None):

    # Composition de la query
    query = """
        SELECT *
        FROM interaction
        WHERE from_user_id = :user_id
        """

    params = {
        "user_id": user_id,
        "limit": limit + 1
    }

    if cursor:
        query += """
            AND (created_at, id) < (:created_at, :interaction_id)
            """

        params["created_at"] = cursor["created_at"]
        params["interaction_id"] = cursor["id"]
    
    query += """
        ORDER BY created_at DESC, id DESC
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