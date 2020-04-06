import os
import psycopg2

APP_NAME = "daniel-reward-bot"
TABLE_NAME = '\'dialog\''
DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a ' + APP_NAME).read()[:-1]


def create_table():
    cmd = 'SELECT * FROM pg_catalog.pg_tables WHERE tablename = ' + TABLE_NAME + ';'
    __query_sql_cmd(cmd)


def __edit_sql_cmd(cmd):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()


def __query_sql_cmd(cmd):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(cmd)
    rows = conn.cursor().fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print()

