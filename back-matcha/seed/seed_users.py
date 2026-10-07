import random
import uuid
from datetime import date, timedelta
import psycopg
from faker import Faker
import numpy as np

fake = Faker("fr_FR")

def generate_password():
    return(fake.password(length=20))

def generate_username():
    return f"{fake.user_name()}_{random.randint(0,800)}"

# --------------------------------------------------
#                   GENERATE USER 
# --------------------------------------------------

def generate_user():
    first_name = fake.first_name()
    last_name = fake.last_name()

    username = generate_username()

    email = f"{first_name}.{last_name}@{fake.domain_word()}.{fake.uri_extension()}"
    signaled = np.random.triangular(0, 0, 5)

    return {
        "id": uuid.uuid4(),
        "email": email,
        "username": username,
        "last_name": last_name,
        "first_name": first_name,
        "password": generate_password(),
        "last_connection": (
            date.today()
            - timedelta(days=random.randint(0, 30))
        ),
        "is_online": random.choice([True, False]),
        "signaled": signaled,
    }



def user(db_conf, nb_users):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()
    user_ids = []
    for _ in range(nb_users):
        user = generate_user()

        # -----------------------------
        # INSERT USER
        # -----------------------------

        cursor.execute(
            """
            INSERT INTO users (
                id,
                email,
                username,
                last_name,
                first_name,
                password,
                last_connection,
                is_online,
                signaled
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                user["id"],
                user["email"],
                user["username"],
                user["last_name"],
                user["first_name"],
                user["password"],
                user["last_connection"],
                user["is_online"],
                user["signaled"],
            ),
        )
        user_ids.append(user["id"])

    connection.commit()

    cursor.close()
    connection.close()
    return user_ids