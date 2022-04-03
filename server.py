#!/usr/bin/env python
from coinsrpc.BitcoinLike import *
import asyncio
import websockets
import simplejson as json

async def chaininfo(websocket):
    name = await websocket.recv()
    print("please  info")
    coin =  Decenomy("sapprpc", "sapprpc", "localhost", 11111)
    if name == "getinfo":
        info = coin.getinfo()
        await websocket.send(json.dumps(info))
    elif name == "list":
        txs = coin.listtxs("*", 500)
        await websocket.send(json.dumps(txs))
    print("sent info")

async def main():
    async with websockets.serve(chaininfo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
