import random
import psycopg
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PICTURES_DIR = BASE_DIR / "pictures"


def generate_pict(user_id, i):
    items = [
        item.name
        for item in PICTURES_DIR.iterdir()
        if item.is_file()
    ]

    if not items:
        raise ValueError(f"Aucune photo trouvée dans {PICTURES_DIR}")

    picture = random.choice(items)
    return {
        "id": i,
        "user_id": user_id,
        "url": f"{picture}",
    }

def pictures(db_conf, user):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()
    nb_pic = []
    for id in user:
        nb = random.randint(0, 5)
        for i in range(nb):
            picture = generate_pict(id, i)
            cursor.execute(
                """
                INSERT INTO pictures(
                    index,
                    user_id,
                    url
                )
                VALUES (
                    %s, %s, %s
                )
                """,
                (
                    picture["id"],
                    picture["user_id"],
                    picture["url"],
                ),
            )
        nb_pic.append(nb)

    connection.commit()

    cursor.close()
    connection.close()
    print("picture table is feed")
    return nb_pic