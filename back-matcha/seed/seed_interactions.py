import random
import psycopg
import uuid
from datetime import date, timedelta

INTERACTION = [
    'Liked',
    'Viewed',
    'Blocked',
]

def generate_interaction(user_id, user):

    to_user_id = random.choice([u for u in user if u != user_id])

    return{
        "id": uuid.uuid4(),
        "from_user_id": user_id,
        "to_user_id": to_user_id,
        "which_interaction": random.choice(INTERACTION),
        "created_at": (
            date.today()
            - timedelta(days=random.randint(0, 30))
        ),
    }

def interactions(db_conf, user):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()
    for user_id in user:
        for _ in range(random.randint(0, 40)):
            interaction = generate_interaction(user_id, user)        
            cursor.execute(
                """
                INSERT INTO interactions(
                    id,
                    from_user_id,
                    to_user_id,
                    which_interaction,
                    created_at
                )
                VALUES (
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    interaction["id"],
                    interaction["from_user_id"],
                    interaction["to_user_id"],
                    interaction["which_interaction"],
                    interaction["created_at"],
                ),
            )


    connection.commit()

    cursor.close()
    connection.close()
    print("interactions are created")
