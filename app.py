from random import choice
from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import debug_vars
from model.flask_sqlalchemy_db import db
# Vars
from model.flask_sqlalchemy_model import Dialog

channelAccessToken = os.environ.get('channelAccessToken')
if debug_vars.dict_vars:
    channelAccessToken = debug_vars.dict_vars["channelAccessToken"]
channelSecret = os.environ.get('channelSecret')
if debug_vars.dict_vars:
    channelSecret = debug_vars.dict_vars["channelSecret"]
DATABASE_URL = os.environ.get('DATABASE_URL')
if debug_vars.dict_vars:
    DATABASE_URL = debug_vars.dict_vars["DATABASE_URL"]


# Flask object
# 本來在sqlalchemy是在create_engine設置的參數，現在搬到這裡來了
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Init DB
db.init_app(app)
with app.app_context():
    db.create_all()

# Line object
# Channel Access Token
line_bot_api = LineBotApi(channelAccessToken)
# Channel Secret
handler = WebhookHandler(channelSecret)


# 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        text = event.message.text
        app.logger.info("Get message: " + text)
        print("Get message: " + text)
        try:
            if text.startswith(CMD_SYMBOL):
                response_text = process_cmd(text)
                app.logger.info("Return response: " + response_text)
                print("Return response: " + response_text)
                message = TextSendMessage(response_text)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                response_list = Dialog.query_response(text)
                if response_list.__len__() > 0:
                    response_text = choice(response_list)[0]
                    app.logger.info("Return response: " + response_text)
                    print("Return response: " + response_text)
                    message = TextSendMessage(response_text)
                    line_bot_api.reply_message(event.reply_token, message)
                else:
                    app.logger.info("Ignore this message.")
                    print("Ignore this message.")
        except Exception as ex:
            s = "完蛋程式有bug了, 錯誤訊息 : \n" + str(ex)
            print(s)
            message = TextSendMessage(s)
            line_bot_api.reply_message(event.reply_token, message)
    return 'OK'


CMD_SYMBOL = "$"
ADD_DIALOG = "新增對話"
DELETE_REQ = "刪除問句"
DELETE_RES = "刪除回答"
QUERY_REQ = "查詢問句"
QUERY_RES = "查詢回答"
QUERY_CMD = "查詢指令"


def process_cmd(text):
    if text.startswith(CMD_SYMBOL):
        text_list = text.split(CMD_SYMBOL)
        del text_list[0]
        for i in text_list:
            if i is None or i == "":
                return "怎麼有某項是空的!!!"

        if text_list[0] == ADD_DIALOG:
            if text_list.__len__() != 3:
                return "格式錯誤，應該是 : " + CMD_SYMBOL + ADD_DIALOG + CMD_SYMBOL + "OOO" + CMD_SYMBOL + "XXX"
            return add_dialog(text_list[1], text_list[2])

        elif text_list[0] == DELETE_REQ:
            if text_list.__len__() != 2:
                return "格式錯誤，應該是 : " + CMD_SYMBOL + DELETE_REQ + CMD_SYMBOL + "OOO"
            return delete_request(text_list[1])

        elif text_list[0] == DELETE_RES:
            if text_list.__len__() != 3:
                return "格式錯誤，應該是 : " + CMD_SYMBOL + DELETE_RES + CMD_SYMBOL + "OOO" + CMD_SYMBOL + "XXX"
            return delete_response(text_list[1], text_list[2])

        elif text_list[0] == QUERY_REQ:
            if text_list.__len__() != 1:
                return "格式錯誤，應該是 : " + CMD_SYMBOL + QUERY_REQ
            return query_request()

        elif text_list[0] == QUERY_RES:
            if text_list.__len__() != 2:
                return "格式錯誤，應該是 : " + CMD_SYMBOL + QUERY_RES + CMD_SYMBOL + "OOO"
            return query_response(text_list[1])

        elif text_list[0] == QUERY_CMD:
            s = ""
            s = s + CMD_SYMBOL + ADD_DIALOG + CMD_SYMBOL + "OOO" + CMD_SYMBOL + "XXX" + "\n"
            s = s + CMD_SYMBOL + DELETE_REQ + CMD_SYMBOL + "OOO" + "\n"
            s = s + CMD_SYMBOL + DELETE_RES + CMD_SYMBOL + "OOO" + CMD_SYMBOL + "XXX" + "\n"
            s = s + CMD_SYMBOL + QUERY_REQ + "\n"
            s = s + CMD_SYMBOL + QUERY_RES + CMD_SYMBOL + "OOO" + "\n"
            return s

        else:
            return "完蛋我看不懂......"


def add_dialog(req, res):
    if Dialog.get_number_of_dialog() > 100:
        return "我要記的問句太多了，有事嗎? 先刪一點掉!!!"
    response_list = Dialog.query_response(req)
    print(response_list)
    if response_list.__len__() == 0:
        Dialog.query_response(req)
    else:
        if response_list.__len__() > 10:
            return "這個問句已經太多種回答了，先刪一點掉!!!"
        elif (res, ) in response_list:
            return "已經新增過了好嗎!!!"

    dialog = Dialog(req, res)
    dialog.add()
    return "新增好了~~~"


def delete_response(req, res):
    if Dialog.check_dialog_is_exist(req, res):
        dialog = Dialog(req, res)
        dialog.delete_response()
        return "刪除完成"
    return "找不到這個回答QAQ"


def delete_request(req):
    if Dialog.query_response(req).__len__() > 0:
        Dialog.delete_request(req)
        return "刪除完成"
    return "找不到這個問句啦!!!"


def query_request():
    request_list = Dialog.query_request()
    if request_list == 0:
        return "空的啦!!!"

    s = "現在聽得懂的問句有 : \n"
    for i in request_list:
        s = s + "<" + i[0] + "> "
    return s


def query_response(req):
    response_list = Dialog.query_response(request=req)
    if response_list.__len__() == 0:
        return "沒有這句啦!!!"

    s = "你說 " + req + ", 我會說:\n"
    for i in response_list:
        s = s + "<" + i[0] + "> "
    return s


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
