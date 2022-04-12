import array
import binascii
import zmq
import struct
import websockets
import asyncio

port = 29000

zmqContext = zmq.Context()
zmqSubSocket = zmqContext.socket(zmq.SUB)
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"hashblock")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"hashtx")
zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

uri = "ws://localhost:8765"
async def zero():

    try:
        while True:
            msg = zmqSubSocket.recv_multipart()
            topic = str(msg[0].decode("utf-8"))
            body = msg[1]
            sequence = "Unknown";

            if len(msg[-1]) == 4:
              msgSequence = struct.unpack('<I', msg[-1])[-1]
              sequence = str(msgSequence)

            if topic == "hashblock":
                block = binascii.hexlify(body).decode("utf-8")
                async with websockets.connect(uri) as websocket:
                    await websocket.send("blockhash:" + block)
            elif topic == "hashtx":
                tx = binascii.hexlify(body).decode("utf-8")
                async with websockets.connect(uri) as websocket:
                    await websocket.send("txid:" + tx)
            #websocket.close()

    except KeyboardInterrupt:
        zmqContext.destroy()

if __name__ == "__main__":
    asyncio.run(zero())
