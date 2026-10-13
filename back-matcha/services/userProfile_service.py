from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError, NotFoundError

PICTURES_FD = "/pictures/"

def get_user_profile_by_id_with_pictures(user_id:str) -> dict:
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    up.user_id,
                    u.username,
                    u.first_name,
                    u.last_name,
                    u.last_connection,
                    u.is_online,
                    up.age,
                    up.gender,
                    up.gender_pref,
                    up.bio,
                    up.popularity,
                    (
                        SELECT JSON_AGG(
                            JSON_BUILD_OBJECT(
                                'id', t.id,
                                'label', t.label
                            )
                        )
                        FROM UNNEST(up.tags) AS tag_id
                        JOIN tags AS t ON t.id = tag_id
                    ) AS tags,
                    up.picture_profile_index,
                    (
                        SELECT ARRAY_AGG(
                            JSON_BUILD_OBJECT(
                                'id', p.index,
                                'url', p.url
                                )
                            )
                        FROM pictures AS p
                        WHERE p.user_id = up.user_id
                    ) AS pictures
                FROM userProfile AS up
                JOIN users AS u ON u.id = up.user_id
                WHERE up.user_id = %s
                """, (user_id,))
            
            userProfileResult = cursor.fetchone()
            
            if not userProfileResult:
                raise NotFoundError
            
            return userProfileResult

    except Exception:
        raise

def get_list_profile_by_id(user_id, limit=20, cursor=None):
    db = get_db()

    query = """
        SELECT
            up.user_id,
            u.username,
            up.age,
            up.localisation AS location,
            u.is_online AS online,
            (
                SELECT JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'id', t.id,
                        'label', t.label
                    )
                )
                FROM UNNEST(up.tags) AS tag_id
                JOIN tags AS t ON t.id = tag_id
            ) AS tags,
            up.bio,
            p.url AS image,
            up.popularity
        FROM userProfile AS up
        JOIN users AS u
            ON u.id = up.user_id
        JOIN pictures AS p
            ON p.user_id = up.user_id
            AND p.index = up.picture_profile_index
        WHERE up.user_id != %s
        AND NOT EXISTS (
            SELECT 1
            FROM blocked AS b
            WHERE
                (b.user_id = %s AND b.user_id_blocked = up.user_id)
                OR
                (b.user_id = up.user_id AND b.user_id_blocked = %s)
        )
    """

    params = [user_id, user_id, user_id]

    if cursor is not None:
        query += " AND up.user_id > %s"
        params.append(cursor)

    query += " ORDER BY up.user_id ASC LIMIT %s"
    params.append(limit + 1)

    with db.cursor() as db_cursor:
        db_cursor.execute(query, tuple(params))
        rows = db_cursor.fetchall()

    # On récupère un profil supplémentaire pour savoir s'il existe
    # une page suivante.
    has_more = len(rows) > limit
    profiles = rows[:limit]

    next_cursor = (
        str(profiles[-1]["user_id"])
        if has_more and profiles
        else None
    )
    print(f"{len(profiles)} profils")
    return {
        "profiles": profiles,
        "next_cursor": next_cursor,
        "has_more": has_more,
    }
