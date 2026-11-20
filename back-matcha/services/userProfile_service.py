
from database.connection import get_db
from utils.exceptions import AppError, NotFoundError, ConflictError




def get_user_profile_by_id_with_pictures(user_id: str) -> dict:
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

                    -- Informations publiques de localisation
                    CASE
                        WHEN loc.user_id IS NOT NULL THEN
                            JSON_BUILD_OBJECT(
                                'city', loc.city,
                                'district', loc.district,
                                'department', loc.department
                            )
                        ELSE NULL
                    END AS location,

                    up.gender,
                    up.gender_pref,
                    up.bio,
                    up.popularity,ConflictError
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

                JOIN users AS u
                    ON u.id = up.user_id

                LEFT JOIN localisation AS loc
                    ON loc.user_id = up.user_id

                WHERE up.user_id = %s
                """, (user_id,))
            ConflictError
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

            -- Informations publiques de localisation
            CASE
                WHEN loc.user_id IS NOT NULL THEN
                    JSON_BUILD_OBJECT(
                        'city', loc.city,
                        'district', loc.district,
                        'department', loc.department
                    )
                ELSE NULL
            END AS location,

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

        LEFT JOIN localisation AS loc
            ON loc.user_id = up.user_id

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

def create_user_profile(dict_info: dict, user_id) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO userProfile (
                    user_id,
                    age,
                    gender,
                    gender_pref,
                    bio,
                    picture_profile_index,
                    localisation,
                    tags
                )
                VALUES (
                    %s,
                    %s::date,
                    %s::gender_type,
                    %s::gender_type[],
                    %s,
                    %s,
                    %s,
                    %s::int[]
                )
                RETURNING
                    user_id,
                    age,
                    gender,
                    gender_pref,
                    bio,
                    picture_profile_index,
                    localisation,
                    tags
                """,
                (
                    str(user_id),
                    dict_info["age"],
                    dict_info["gender"],
                    dict_info["gender_pref"],
                    dict_info["bio"],
                    dict_info["picture_profile_index"],
                    dict_info["localisation"],
                    dict_info["tags"],
                ),
            )
            profile = cursor.fetchone()

        db.commit()
        return profile

    except IntegrityError:
        db.rollback()
        raise ConflictError("Profile already exists or user not found")

    except Exception:
        db.rollback()
        raise