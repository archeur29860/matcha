import psycopg

def request_SQL(cursor):
    cursor.execute(
        """
        INSERT INTO matches(
        id,
        user_low_id,
        user_high_id,
        created_at
        )
        SELECT
            gen_random_uuid(),
            i.from_user_id,
            i.to_user_id,
            GREATEST(i.created_at, reciprocal.created_at)
        FROM interactions i
        JOIN interactions reciprocal
            ON reciprocal.from_user_id = i.to_user_id
            AND reciprocal.to_user_id = i.from_user_id
        WHERE i.which_interaction = 'Liked'
            AND reciprocal.which_interaction = 'Liked'
            AND i.from_user_id < i.to_user_id
        ON CONFLICT (user_low_id, user_high_id) DO NOTHING;
        """
        )


def match(db_conf):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()
    request_SQL(cursor)
    connection.commit()

    cursor.close()
    connection.close()
    print("match table is fell")
