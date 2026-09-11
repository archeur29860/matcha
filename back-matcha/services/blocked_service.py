from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

import traceback

def insert_relation(user_id, user_id_blocked):

    try:
        result = db.session.execute(
            text("""
                INSERT INTO blocked (user_id, user_id_blocked)
                VALUES (:user_id, :user_id_blocked)
                RETURNING user_id, user_id_blocked
                """),
            {"user_id": user_id,
            "user_id_blocked": user_id_blocked
            })

        relation = result.mappings().one()
        db.session.commit()
        return dict(relation)

    except Exception as e:
        db.session.rollback()
        print("===== ERREUR =====")
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        traceback.print_exc()
        return None