
from seed_users import user
from seed_profiles import profile
from seed_pictures import pictures
from seed_interactions import interactions
from seed_matches import match
from seed_situgeo import situgeo

# from seed_messages import message

import os
import psycopg


# --------------------------------------------------
#                   CONFIGURATION
# --------------------------------------------------

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}


# --------------------------------------------------
#                   DATABASE CHECK
# --------------------------------------------------

def request_sql(cursor):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users;
        """
    )
    return cursor.fetchone()[0]


def check_nb_users_created():
    connection = psycopg.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            nb_user = request_sql(cursor)

        return nb_user <= 500

    finally:
        connection.close()


# --------------------------------------------------
#                   MAIN SEED
# --------------------------------------------------

def main():

    if check_nb_users_created():

        nb_user = int(os.environ["NB_FAKE_PROFILE"])

        # 1. Création des utilisateurs
        users_id = user(DB_CONFIG, nb_user)

        # 2. Création des localisations
        situgeo(
            db_conf=DB_CONFIG,
            user_ids=users_id,
            radius_meters=150
        )

        # 3. Création des photos
        nbs_picture = pictures(DB_CONFIG, users_id)

        # 4. Création des profils
        profile(
            DB_CONFIG,
            users_id,
            nbs_picture
        )

        # 5. Création des interactions
        interactions(DB_CONFIG, users_id)

        # 6. Création des matchs
        match(DB_CONFIG)

        # 7. Création des messages
        # message(DB_CONFIG)

        print(f"Seed terminé : {len(users_id)} utilisateurs créés.")

    else:
        print(
            "Seed annulé : la base contient déjà plus de 500 utilisateurs."
        )


# --------------------------------------------------
#                   EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    main()
