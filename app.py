from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
# import button api
from linebot.models import ButtonsTemplate, MessageTemplateAction, TemplateSendMessage, PostbackTemplateAction
# import quick reply
from linebot.models import QuickReply, QuickReplyButton, LocationAction

import configparser
import re

import view

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))


@app.route("/callback", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=LocationMessage)
# TextMessage
def handle_message(event):
    try:
        text = event.TextMessage.text
    except:
        text = event.LocationMessage.address
    print(text)
    reply_all = []

    # pattern_en = re.compile('Q:(.+)')
    # pattern_zh = re.compile('問題:(.+)')

    # if pattern_en.findall(text):
    #     tokens = pattern_en.findall(text)
    #     en_ques = tokens[0]

    #     max_sim, doc_sim = get_en_doc_similarity(en_ques)
    #     if max_sim >= 0.9:
    #         response = "Your question is similar to:\n\""+doc_sim + \
    #             "\".\nThis similarity score is \""+str(max_sim)+"\"."
    #     else:
    #         response = "I do not understand your question.\nPlease rephrase your question."

    # elif pattern_zh.findall(text):
    #     tokens = pattern_zh.findall(text)
    #     zh_ques = tokens[0]

    #     max_sim, doc_sim = get_zh_doc_similarity(zh_ques)
    #     if max_sim >= 0.5:
    #         response = "Your question is similar to:\n\""+doc_sim + \
    #             "\".\nThis similarity score is \""+str(max_sim)+"\"."
    #     else:
    #         response = "I do not understand your question.\nPlease rephrase your question."

    # else:

    #     reply_all.append(TextSendMessage(text="格式錯誤!!!"))
    #     response = '<<英文問題格式>>\n"Q:XXX"\n\n<<中文問題格式>>\n"問題:XXX"'

    # response = "你好！我是美食推薦機器人，很高興為你服務，可以傳送你現在位置的資訊給我嗎"
    # reply_all.append(TextSendMessage(text=response))

    # 回覆文字訊息
    # line_bot_api.reply_message(event.reply_token, reply_all)
    # 回復按鈕訊息
    message = view.location()
    # message = view.transport()
    # message = view.google_api()
    data = view.google_api(22.996638325747668, 120.21665748163963, 1500, "咖哩")
    line_bot_api.reply_message(
        event.reply_token, message)


if __name__ == "__main__":
    app.run(debug=True)
