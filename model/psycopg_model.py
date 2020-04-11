import os
import psycopg2

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

APP_NAME = "daniel-reward-bot"
TABLE_NAME = '\'dialog\''
# DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = "postgres://jvzcophjjmmtrw:e55849bcd059162ab48a1432b82c66dae07cb3aeeb6b14b22ca24f7b7c97143c@ec2-54-159-112-44.compute-1.amazonaws.com:5432/duiro8fleg79"


class DialogModel:
    def __init__(self):
        print(self.__show_all_table())
        # if not self.__check_table_exist():
        #     self.__create_table()

    def __create_table(self):
        cmd = "CREATE TABLE " + TABLE_NAME + "('request char', 'response' char);"
        self.__edit_sql_cmd(cmd)

    def __show_all_table(self):
        cmd = "select * from information_schema.tables where table_schema = 'public';"
        return self.__query_sql_cmd(cmd)

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


Base = declarative_base()


# 這裡宣告class，所有繼承base的class都會在base裡面註冊一個table，所以class的靜態變數__tablename__是必備的
class User(Base):
    __tablename__ = 'dialog2'
    request = Column(String, primary_key=True)
    response = Column(String, nullable=False)


class User2(Base):
    __tablename__ = 'dialog3'
    request = Column(String, primary_key=True)
    response = Column(String, nullable=False)

#
# engine = create_engine(DATABASE_URL)
#
# # 這一行應該是base會根據engine去找前面註冊過的table，如果有就match一下，沒有就create一個
# Base.metadata.create_all(engine)
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


class A:
    a = 100

if __name__ == "__main__":

    a = A()
    b = A()
    print(A.a)
    print(a.a)
    print(b.a)
    A.a = 999
    print(A.a)
    print(a.a)
    print(b.a)
    a.a = 222
    print(A.a)
    print(a.a)
    print(b.a)