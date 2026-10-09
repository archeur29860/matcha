from psycopg.errors import IntegrityError

from database.connection import get_db
from utils.exceptions import AppError, NotFoundError

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
                                'index', p.index,
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