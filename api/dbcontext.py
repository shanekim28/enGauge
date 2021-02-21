import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure

conn_string = f"postgres://sdhacks:sdhacks21gang@firm-bull-8m3.gcp-us-west2.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=/Users/shane/Downloads/firm-bull-ca.crt"

conn = None


def init():
    global conn
    conn = psycopg2.connect(conn_string)


def create_user(discordid, firstname, lastname):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (discordid VARCHAR PRIMARY KEY, firstname VARCHAR, lastname VARCHAR, points INT)"
        )

        try:
            cur.execute(
                "INSERT INTO users (discordid, firstname, lastname, points) VALUES (%s, %s, %s, %s);", (discordid, firstname, lastname, 0))
        except:
            pass

        logging.debug("create_user(): status message: %s", cur.statusmessage)
    conn.commit()


def delete_users():
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.users")
        logging.debug("delete_accounts(): status message: %s",
                      cur.statusmessage)
    conn.commit()


def get_leaderboard():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT firstname, lastname, points FROM users ORDER BY points DESC, firstname ASC")
        rows = [dict((cur.description[i][0], value)
                     for i, value in enumerate(row)) for row in cur.fetchall()]
        conn.commit()
        return rows


def add_points(id, amount):
    with conn.cursor() as cur:
        cur.execute("SELECT points FROM users WHERE discordid = %s", (id,))
        if (not cur.fetchone()):
            print("User not registered")
            conn.commit()
            return
        currentpoints = cur.fetchone()
        cur.execute(
            "UPDATE users SET points = points + %s WHERE discordid = %s", (amount, id))

    conn.commit()
