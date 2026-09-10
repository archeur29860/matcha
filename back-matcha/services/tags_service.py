from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db

def add_tag(new_label):

    try :
        result = db.session.execute(
            text("INSERT INTO tags (label) VALUES (:n_label)\
            RETURNING id, label"),
            {"n_label": new_label}
        )

        tags = result.mappings().one()
        db.session.commit()
        return dict(tags)

    except IntegrityError:
        db.session.rollback()
        return None


def get_all_tags():
    result = db.session.execute(
        text("SELECT * FROM tags")
    )

    tags = result.mappings()
    return tags.all()