import random
import psycopg
import os

def generate_pict(user_id, i):
    items = os.listdir("../pictures")
    nb_items = len(items)
    picture = items[random.randint(0, nb_items - 1)]

    return{
        "index": i,
        "user_id": user_id,
        "url": f"../pictures/{picture}",
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
    return nb_pic