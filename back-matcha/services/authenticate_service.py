from database.connection import get_db

def get_authenticate_user(email):
    db = get_db()

    query = """
        SELECT
            id,
            email,
            username,
            last_name,
            first_name,
            password
        FROM users
        WHERE email = %s
    """

    try:
        with db.cursor() as cursor_db:
            cursor_db.execute(query, (email,))
            user = cursor_db.fetchone()

        return user

    except Exception:
        db.rollback()
        raise


def get_user_by_id(user_id):
    db = get_db()

    query = """
        SELECT
            id,
            email,
            username,
            last_name,
            first_name
        FROM users
        WHERE id = %s
    """
    try:
        with db.cursor() as cursor_db:
            cursor_db.execute(query, (user_id,))
            user = cursor_db.fetchone()

        return user
    except Exception:
        db.rollback()
        raise