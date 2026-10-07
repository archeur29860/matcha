from seed_users import user
from seed_profiles import profile
from seed_pictures import pictures
from seed_interactions import interactions
from seed_matches import match
# from seed_messages import message
import os

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

NB = 500

def main():
    users_id = user(DB_CONFIG, NB)
    nbs_picture = pictures(DB_CONFIG, users_id)
    profiles = profile(DB_CONFIG, users_id, nbs_picture)
    interactions(DB_CONFIG, users_id)
    match(DB_CONFIG)
    # seed_messages(DB_CONFIG, interactions)


if __name__ == "__main__":
    main()