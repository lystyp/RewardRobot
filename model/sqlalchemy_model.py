import os
import time

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import debug_vars

APP_NAME = "daniel-reward-bot"
TABLE_NAME = '\'dialog\''
DATABASE_URL = os.environ.get('DATABASE_URL')
if debug_vars.dict_vars:
    DATABASE_URL = debug_vars.dict_vars["DATABASE_URL"]


Base = declarative_base()
engine = create_engine(DATABASE_URL)
# session就是跟sql連上後的操作負責人
session = sessionmaker(bind=engine)()


# 這裡宣告class，所有繼承base的class都會在base裡面註冊一個table，所以class的靜態變數__tablename__是必備的
# 如果table存在但static變數與table欄位不符，或是column的型態不符，會error，如果單純屬性不符，會以table為主，不理class裡的Column參數
class DialogModel(Base):
    __tablename__ = 'dialog'
    request = Column(String, primary_key=True, nullable=False)
    response = Column(String, primary_key=True, nullable=False)


# 這一行應該是base會根據engine去找前面註冊過的table，如果表格已經存在sql裡，那這行有跟沒有就醫樣了啊(不會work)!!!!沒有就create一個
# create 是根據class的static變數去創建column的，
# 但new 一個class實體去add資料的時候，則是去找class的實體的成員來add的，所以我new完DialogModel用實體去更改request再add，其實還是有用
# Base.metadata.create_all(engine)


if __name__ == "__main__":
    TEST_PART = 1

    # 測試session操作
    if TEST_PART == 1:
        # 為什麼明明是全域變數，卻可以這樣給參數呢?因為繼承Base時Base裡面有動一點手腳
        dialog = DialogModel(request='你好!!', response="有事?")
        # 下面這行會work!!!現在實體也有response成員了!從實體就找的到dialog.response，就會直接新增這個
        # 如果實體沒有response成員，dialog.response才會是拿到class的static變數
        session.add(dialog)
        session.commit()

    # engine connection pool 操作測試
    elif TEST_PART == 2:
        engine = create_engine(DATABASE_URL, pool_size=5)
        t_s = time.time()
        sess_list = []
        for i in range(2):
            session = engine.connect()
            sess_list.append(session)
            print("Done > " + str(i) + " > " + str(session))
            print(time.time() - t_s)
            t_s = time.time()

        for item in sess_list:
            item.close()
        print("Again~~~~~~~~~~~~~~~~~~~~~~~~~~")
        t_s = time.time()
        sess_list = []
        for i in range(5):
            session = engine.connect()
            sess_list.append(session)
            print("Done > " + str(i) + " > " + str(session))
            print(time.time() - t_s)
            t_s = time.time()

    elif TEST_PART == 3:
        query_result = session.query(DialogModel).all()
        print(query_result[0].request)
        print(query_result[0].response)

        # 還有其他種查詢的方法：
        # session.query(User).all()
        # session.query(User).filter(User.id == 1)
    print("Done")


