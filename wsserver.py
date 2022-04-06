from coinsrpc.BitcoinLike import *
import asyncio
import websockets
import simplejson as json

async def chaininfo(websocket):
    name = await websocket.recv()
    
    coin =  Decenomy("sapprpc", "sapprpc", "localhost", 11111) #to do, get the info from somewhere else

    if name.startswith("blockhash") == True:
        bhash = name.split(":")[1]
        info = coin.block(bhash)
        await websocket.send(json.dumps(info))    
    elif name.startswith("txid") == True:
        txid = name.split(":")[1]
        try:
            tx = coin.gettx(txid)
            await websocket.send(json.dumps(tx))
        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))

async def main():
    async with websockets.serve(chaininfo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
