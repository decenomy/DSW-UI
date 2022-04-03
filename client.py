import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("getinfo")

        greeting = await websocket.recv()
        print(greeting)

if __name__ == "__main__":
    asyncio.run(hello())
