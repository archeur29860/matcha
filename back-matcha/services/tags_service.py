from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

def insert_tag(new_label):

    try :
        result = db.session.execute(
            text("INSERT INTO tags (label) VALUES (:n_label)\
            RETURNING id, label"),
            {"n_label": new_label}
        )

        tag = result.mappings().one()

        db.session.commit()

        return dict(tag)

    except IntegrityError:
        db.session.rollback()
        raise ConflictError(
            "Resource already exists"
        )

    except Exception:
        db.session.rollback()
        raise


def get_all_tags():
    try :
        result = db.session.execute(
            text("SELECT * FROM tags \
            ORDER BY label ASC")
        )

        tags = result.mappings().all()

        return [dict(tag) for tag in tags]

    except Exception:
        db.session.rollback()
        raise