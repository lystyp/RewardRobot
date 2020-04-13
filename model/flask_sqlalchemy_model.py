import os
import debug_vars
from model.flask_sqlalchemy_db import db

APP_NAME = "daniel-reward-bot"
TABLE_NAME = '\'dialog\''
DATABASE_URL = os.environ.get('DATABASE_URL')
if debug_vars.dict_vars:
    DATABASE_URL = debug_vars.dict_vars["DATABASE_URL"]


class Dialog(db.Model):
    # db.Modle的Table name沒有取會預設用class名字轉小寫加底線
    __tablename__ = 'dialog'
    request = db.Column(db.String, primary_key=True, nullable=False)
    response = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, request, response):
        self.request = request
        self.response = response

    def add(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def check_dialog_is_exist(cls, request, response):
        return cls.query.filter_by(request=request, response=response).scalar() is not None

    @classmethod
    def get_number_of_dialog(cls):
        return cls.query.count()

    @classmethod
    def query_request(cls):
        return cls.query.with_entities(cls.request).all()

    @classmethod
    def query_response(cls, request):
        # This function will return a tuple list.
        return cls.query.with_entities(cls.response).filter_by(request=request).all()

    @classmethod
    def delete_request(cls, request):
        # 應該要有別的比較漂亮的方法才對!!!
        db.session.query(cls).filter(cls.request == request).delete()
        db.session.commit()

    # TODO
    # 有一個bug但我解不出來，只用奇怪的解法
    # https://stackoverflow.com/questions/26597755/invalidrequesterror-instance-user-at-0x7f65938a7510-is-not-persisted
    # def delete_response(self):
    #     db.session.delete(self)
    #     db.session.commit()

    @classmethod
    def delete_response(cls, request, response):
        # 應該要有別的比較漂亮的方法才對!!!
        db.session.query(cls).filter(cls.request == request, cls.response == response).delete()
        db.session.commit()
