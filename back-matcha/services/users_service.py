from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import db


def add_user(dict_info):

    try :
        result = db.session.execute(
            text("""
                INSERT INTO users (
                    email,
                    username,
                    last_name,
                    first_name,
                    password) 
                VALUES (
                    :n_email,
                    :n_username,
                    :n_last_name, 
                    :n_first_name, 
                    :n_password)
                RETURNING id, email
            """),
            {
                "n_email": dict_info["email"],
                "n_username": dict_info["username"], 
                "n_last_name": dict_info["last_name"], 
                "n_first_name": dict_info["first_name"], 
                "n_password": dict_info["password"], 
             }
             )

        user = result.mappings().one()
        db.session.commit()
        return dict(user)
    
    except IntegrityError:
        db.session.rollback()
        raise AppError(
            code="USER_ALREADY_EXISTS",
            message="user_already exists",
            status_code=409
        )
        
    except Exception:
        db.session.rollback()
        raise

# Modify

def modify_user( dict_info):

    try :
        result = db.session.execute(
            text("""
                UPDATE users SET
                    email = :n_email,
                    username = :n_username,
                    last_name = :n_last_name,
                    first_name = :n_first_name,
                    password = :n_password
                WHERE id = :user_id
                RETURNING id, email
            """),
            {
                "user_id": dict_info["user_id"],
                "n_email": dict_info["email"],
                "n_username": dict_info["username"], 
                "n_last_name": dict_info["last_name"], 
                "n_first_name": dict_info["first_name"], 
                "n_password": dict_info["password"], 
             }
        )

        user = result.mappings().first()

        if user is None:
            db.session.rollback()
            raise AppError(
                        code="USER_DOESNT_EXISTS",
                        message="user doesn't exists",
                        status_code=404
                    )

        db.session.commit()
        
        return dict(user)

    except IntegrityError:
        db.session.rollback()
        raise AppError(
            code="USER_ALREADY_EXISTS",
            message="user_already exists",
            status_code=409
        )
        
    except Exception:
        db.session.rollback()
        raise

# def add_email(new_email):

#     try :
#         result = db.session.execute(
#             text("INSERT INTO users (email) VALUES (:n_email)\
#             RETURNING id, email"),
#             {"n_email": new_email}
#         )

#         mail = result.mappings().one()
#         db.session.commit()
#         return dict(mail)

#     except IntegrityError:
#         db.session.rollback()
#         return None


# def get_all_tags():
#     result = db.session.execute(
#         text("SELECT * FROM tags")
#     )

#     tags = result.mappings()
#     return tags.all()
# # GETTER



# def get_user(id_user):
#     result = db.session.execute(
#         text("SELECT id, email, username, last_name," \
#         "first_name, password FROM users WHERE id = id_user;")
#     )

#     user = result.mappings()
#     return dict(user)

# def get_user_external(id_user_ex):
#     result = db.session.execute(
#         text("SELECT id, username, last_name, first_name, is_online " \
#         "FROM users" \
#         "WHERE id = id_user_ex;")
#     )

#     user = result.mappings()
#     return dict(user)