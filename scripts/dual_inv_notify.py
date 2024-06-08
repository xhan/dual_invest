import requests
import asyncio
import json
import pandas as pd
from binance.spot import Spot
import json
import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

BotToken =  os.getenv('BotToken')
BN_KEY = os.getenv('BN_KEY')
BN_SECRET = os.getenv('BN_SECRET')
CHAT_ID = os.getenv('CHAT_ID')
# SleepTime = 60
SleepTime = 10
"""  脚本说明：

    1. 读取 binance 双币投资的持仓
    2. 跟踪变化， 发现变化后，通过 tg 机器人发送消息

"""

def get_chat_id():
    # 1124758403  user_id  name :janeybb
    url = f'https://api.telegram.org/bot{BotToken}/getUpdates'
    response = requests.get(url)
    print(response.json())


def send_msg(chat_id, msg):
    url = f'https://api.telegram.org/bot{BotToken}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': msg
    }
    response = requests.post(url, data=data)
    print(response.json())


# get_chat_id()
# send_msg(1124758403,"nice to seee you!")



def get_dual_assets_list():

    # xuhan3000 read only
    client = Spot(api_key="2HEmLJI5c9JONYywRIXhsTr3T3oWjY919aqhMEvesjjt8OrjjveKYp3C0z79w7xW", api_secret="ctwbTokSYdHf7opFOaUo8jMP1GHjlWTGW6kvhBrfkMerRvhAfbeokLrg34qZjXOy")
    # 获取双币列表，注意 100 条可能不全，后续改成读取所有
    ret = client.sign_request("GET","/sapi/v1/dci/product/positions",{'pageSize':100})

    df = pd.DataFrame(ret["list"])
    df['settleDate'] = df['settleDate'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d'))
    df['purchaseEndTime'] = df['purchaseEndTime'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d'))
    df.set_index('id', inplace=True)
    df.drop(["orderId","optionType","autoCompoundPlan","purchaseEndTime"],axis=1, inplace=True)

    # 过滤 purchaseStatus 为 PURCHASE_SUCCESS or SETTLING 
    df = df[(df['purchaseStatus'] == 'PURCHASE_SUCCESS') | (df['purchaseStatus'] == 'SETTLING')]
    print(df[:2])
    return df


origin_df = get_dual_assets_list()
time.sleep(SleepTime)
while True:
    df_now = get_dual_assets_list()    
    # 判断同 id 的项目，purchaseStatus 是否发生变化
    df = df_now.merge(origin_df["purchaseStatus"].to_frame(), on='id', how="left", suffixes=('_new', '_old'))
    print(df[:5])

    df = df[df['purchaseStatus_old'] != df['purchaseStatus_new']]

    if len(df) > 0:
        print("=== Change founded!!!!!")
        print(df)
        send_msg(CHAT_ID,f"Changed record : {len(df)}\n" + df.T.to_string())
        origin_df = df_now
    else:
        print("=== Change not found = =")

    time.sleep(SleepTime)

    