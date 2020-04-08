import os
import psycopg2

APP_NAME = "daniel-reward-bot"
TABLE_NAME = '\'dialog\''
DATABASE_URL = os.environ.get('DATABASE_URL')


class DialogModel:
    def __init__(self):
        if not self.__check_table_exist():
            self.__create_table()

    def __create_table(self):
        cmd = "CREATE TABLE " + TABLE_NAME + "('request char', 'response' char);"
        self.__edit_sql_cmd(cmd)

    def __check_table_exist(self):
        cmd = 'SELECT * FROM pg_catalog.pg_tables WHERE tablename = ' + TABLE_NAME + ';'
        result = self.__query_sql_cmd(cmd)
        return result.__len__() > 0

    def __edit_sql_cmd(self, cmd):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(cmd)
        conn.commit()
        conn.close()

    def __query_sql_cmd(self, cmd):
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(cmd)
        rows = cursor.fetchall()
        conn.close()
        return rows


if __name__ == "__main__":
    pass

