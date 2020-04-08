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
import model

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('channelAccessToken'))
# Channel Secret
handler = WebhookHandler(os.environ.get('channelSecret'))


dialog_dict = {}


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
            elif text in dialog_dict:
                response_text = choice(dialog_dict[text])
                app.logger.info("Return response: " + response_text)
                print("Return response: " + response_text)
                message = TextSendMessage(response_text)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                app.logger.info("Ignore this message.")
                print("Ignore this message.")
        except Exception as ex:
            s = "完蛋程式有bug了, 錯誤訊息 : \n" + str(ex)
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
    if dialog_dict.__len__() > 100:
        return "我要記的問句太多了，有事嗎? 先刪一點掉!!!"

    if req not in dialog_dict:
        dialog_dict[req] = [res]
    else:
        if dialog_dict[req].__len__() > 10:
            return "這個問句已經太多種回答了，先刪一點掉!!!"
        if res not in dialog_dict[req]:
            dialog_dict[req].append(res)
        else:
            return "已經新增過了好嗎!!!"

    return "新增好了~~~"


def delete_response(req, res):
    if req in dialog_dict:
        if res in dialog_dict[req]:
            dialog_dict[req].remove(res)
            if dialog_dict[req].__len__() == 0:
                dialog_dict.pop(req)
            return "刪除完成"
    return "找不到這個回答QAQ"


def delete_request(req):
    if req in dialog_dict:
        dialog_dict.pop(req)
        return "刪除完成"
    return "找不到這個問句啦!!!"


def query_request():
    if dialog_dict.__len__() == 0:
        return "空的啦!!!"

    s = "現在聽得懂的問句有 : \n"
    for i in dialog_dict.keys():
        s = s + "<" + i + "> "
    return s


def query_response(req):
    if req not in dialog_dict:
        return "沒有這句啦!!!"

    s = "你說 " + req + ", 我會說:\n"
    for i in dialog_dict[req]:
        s = s + "<" + i + "> "
    return s


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
