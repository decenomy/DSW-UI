from coinsrpc.BitcoinLike import *
import asyncio
import websockets
import simplejson as json

USERS = set()

async def chaininfo(websocket):
    global USERS
    USERS.add(websocket)
    
    name = await websocket.recv()
    print(name)
    coin =  Decenomy("sapprpc", "sapprpc", "localhost", 11111) #to do, get the info from somewhere else

    if name.startswith("blockhash") == True:
        bhash = name.split(":")[1]
        info = coin.block(bhash)
        websockets.broadcast(USERS, json.dumps(info))
        await websocket.send(json.dumps(info))    
    elif name.startswith("txid") == True:
        txid = name.split(":")[1]
        try:
            tx = coin.gettx(txid)
            websockets.broadcast(USERS, json.dumps(tx))
            await websocket.send(json.dumps(tx))
        except Exception as e:
            websockets.broadcast(USERS, json.dumps({"error": str(e)}))
            await websocket.send(json.dumps({"error": str(e)}))
    for u in USERS:
        print(u)
    USERS.remove(websocket)

async def main():
    async with websockets.serve(chaininfo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())