import random
import psycopg
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PICTURES_DIR = BASE_DIR / "pictures"


def generate_pict(user_id, i):
    items = os.listdir(PICTURES_DIR)
    nb_items = len(items)
    picture = items[random.randint(0, nb_items - 1)]

    return{
        "index": i,
        "user_id": user_id,
        "url": f"PICTURES_DIR{picture}",
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
                    picture["index"],
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