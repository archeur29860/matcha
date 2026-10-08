from database.connection import get_db


def get_authenticate_user():
    db = get_db()
    query = """
        SELECT
            email,
            password
        FROM users
        """
    try:
        with db.cursor() as cursor_db:
            cursor_db.excute(query)
            users = cursor_db.fetchall()
        return users

    except Exception:
        db.rollback()