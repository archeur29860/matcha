from database.connection import get_db

def get_authenticate_user(email):
    db = get_db()

    query = """
        SELECT
            id,
            email,
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