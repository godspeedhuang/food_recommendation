from linebot.models import *
import requests
import json


def location():
    message = TextSendMessage(text="你好，我是美食機器人，請告訴我你在所在位置，我將會為您推薦好吃的食物!",
                              quick_reply=QuickReply(items=[
                                  QuickReplyButton(action=LocationAction(label="查詢目前所在位置"))])
                              )
    return message


def transport():
    message = TemplateSendMessage(
        alt_text='交通運具選擇方式',
        template=ButtonsTemplate(
            title='交通工具',
            text='請問您使用的交通運具種類為何呢？',
            actions=[
                MessageTemplateAction(
                    label='步行',
                    text='步行',
                    # data=""
                ),
                MessageTemplateAction(
                    label='單車',
                    text='單車',
                    # data=''
                ),
                MessageTemplateAction(
                    label='機車',
                    text='機車',
                    # data=''
                ),
                MessageTemplateAction(
                    label='汽車',
                    text='汽車',
                    # data=''
                )
            ]
        )
    )
    return message

# 取得周邊餐廳資料


def google_api(lat, lng, r, keyword):
    API = "AIzaSyBXioCZJv01QRXxBedIqkjSeC2ilJY3TVU"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lng}&radius={r}&type=restaurant&keyword={keyword}&key={API}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    max = 0
    for i in response['results']:
        if(float(i['rating']) > max):
            max = float(i['rating'])
            place_id = i['place_id']
    POI_url = __get_poi_url(place_id, API=API)
    # 整理json資料
    return POI_url


# 取得前述餐廳中評分最高的google map url
def __get_poi_url(place_id, API):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name%2Curl&key={API}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    POI_url = response['result']['url']
    return POI_url


if(__name__ == "__main__"):
    pass
