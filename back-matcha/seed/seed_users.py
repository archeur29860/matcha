import random
import uuid
from datetime import date, timedelta
import psycopg
from faker import Faker
import numpy as np
import csv
from werkzeug.security import generate_password_hash

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

    email = f"{first_name}.{last_name}@{fake.domain_word()}{fake.uri_extension()}"
    signaled = np.random.triangular(0, 0, 5)
    password= generate_password()
    pwd_hash= generate_password_hash(password)

    return {
        "id": uuid.uuid4(),
        "email": email,
        "username": username,
        "last_name": last_name,
        "first_name": first_name,
        "password": password,
        "pwd_hash": pwd_hash,
        "last_connection": (
            date.today()
            - timedelta(days=random.randint(0, 30))
        ),
        "is_online": random.choice([True, False]),
        "signaled": signaled,
    }

def generate_csv(user, filename="fake_user.csv"):

    fieldnames = [
        "id",
        "email",
        "username",
        "last_name",
        "first_name",
        "password",
        "pwd_hash",
        "last_connection",
        "is_online",
        "signaled",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerow(user)

    print(f"1 user is {filename}")


def user(db_conf, nb_users):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()
    user_ids = []

    for _ in range(nb_users):
        user = generate_user()
        if _ == 0:
            generate_csv(user)
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
                user["pwd_hash"],
                user["last_connection"],
                user["is_online"],
                user["signaled"],
            ),
        )
        user_ids.append(user["id"])

    connection.commit()

    cursor.close()
    connection.close()
    print(f"{nb_users} users are created")
    return user_ids