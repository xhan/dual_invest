from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles


from binance import AsyncClient 
from dotenv import load_dotenv
import os
import json

load_dotenv()

BN_KEY = os.getenv('BN_KEY')
BN_SECRET = os.getenv('BN_SECRET')

app = FastAPI()




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

"""
return 
        {
        symbol: "BTCUSDT",
        price: "67434.35000000"
        }
"""
@app.websocket("/price/{symbol}")
async def get_price(websocket: WebSocket , symbol:str):
    symbol = symbol.upper()

    await websocket.accept()
    while True:
        client = await AsyncClient.create(BN_KEY, BN_SECRET)
        ret = await client.get_symbol_ticker(symbol=symbol.upper())
        await websocket.send_text(json.dumps(ret, indent=4))
        await websocket.receive_text()



"""
/btc/sp /btc/sc 
"""
@app.websocket('/{coin}/{type}')
async def websocket_dual_invest(websocket: WebSocket, coin: str, type: str):
    if coin not in ['btc', 'eth'] or type not in ['sp', 'sc']:
        await websocket.close(code=1008)  # 关闭连接并返回错误码
        return

    client = await AsyncClient.create(BN_KEY, BN_SECRET)
    await websocket.accept()
    while True:
        ret = await get_dual_list(client,pageIndex=1,pageSize=100,coin=coin,type=type)
        size = ret['total']
        print("total size:",size)        
        print("contents count",len(ret['list']))
        pages = size // 100 + 1
        await websocket.send_text(json.dumps(ret, indent=4))

        for i in range(pages - 1):
            ret = await get_dual_list(client,pageIndex=i+2,pageSize=100,coin=coin,type=type)
            print("contents count at page ",i+2, len(ret['list']))
            await websocket.send_text(json.dumps(ret, indent=4))

        data = await websocket.receive_text()


@app.get("/json")
async def get_json():
    client = await AsyncClient.create(BN_KEY, BN_SECRET)
    return await get_dual_list(client,pageIndex=1,pageSize=100)     


#Get Dual Investment product list(USER_DATA)
# 获取可以投资列表

async def get_dual_list(client,pageSize=100, pageIndex=1,coin:str = 'btc' ,type:str = 'sc'):
    coin = coin.upper()
    type = type.upper()
    if(type == 'SC'):
        params = {
        "optionType": "CALL",  # PUT
        "exercisedCoin": "USDT",
        "investCoin": coin, 
        }
    else:
        params = {
        "optionType": "PUT",  # PUT
        "exercisedCoin": coin,
        "investCoin": "USDT",
        }
    
    params.update({
        "pageSize":pageSize,
        "pageIndex":pageIndex  
    })
    print(params)

    return await client._request_margin_api('get', '/dci/product/list', True, data=params)
    # return ret




# @app.get("/")
# async def get():
#     return {"message": "Hello World"}

app.mount('/',StaticFiles(directory='server/public', html=True), name='public')
    