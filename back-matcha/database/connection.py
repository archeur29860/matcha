from flask import g
import os
import psycopg
from psycopg.rows import dict_row


def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            row_factory=dict_row,
        )

    return g.db


def close_db(exception=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()