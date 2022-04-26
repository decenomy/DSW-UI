from coinsrpc.BitcoinLike import *
import sys
import asyncio
import websockets
import simplejson as json
from datetime import datetime

USERS = set()

ticker = sys.argv[1]

with open('settings.json') as json_file:
    app_settings = json.load(json_file)

async def chaininfo(websocket):
    global USERS
    USERS.add(websocket)
    try:
        name = await websocket.recv()
    except websockets.ConnectionClosedOK:
        name = ''
        pass
    c = app_settings["coins"][selected_coin]
    coin =  Decenomy(c["rpcuser"], c["rpcpassword"], c["host"], c["rpcport"])

    if name.startswith("blockhash") == True:
        bhash = name.split(":")[1]
        info = coin.block(bhash)
        websockets.broadcast(USERS, json.dumps({"type":"block", "data":info})) 
    elif name.startswith("txid") == True:
        txid = name.split(":")[1]
        try:
            tx = coin.gettx(txid)
            dt_object = datetime.fromtimestamp(tx["time"])
            tx["time"] = str(dt_object)
            websockets.broadcast(USERS, json.dumps({"type":"transaction", "data":tx}))
        except Exception as e:
            websockets.broadcast(USERS, json.dumps({"error": str(e)}))

    w_info = coin.getinfo()
    websockets.broadcast(USERS, json.dumps({"type":"getinfo", "data":w_info}))


    USERS.remove(websocket)

async def main():
    async with websockets.serve(chaininfo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
