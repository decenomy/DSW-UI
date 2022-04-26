## Python web UI for DSW

The UI currently requires python >=3.7

First clone the repo and install requirements:

```
pip3 install -r requirements.txt

```

Add the following lines  in your coin.conf file:

```
zmqpubrawtx=tcp://127.0.0.1:29000
zmqpubhashtx=tcp://127.0.0.1:29000
```

Edit settings.json file with your own password and rpc configurations:

```
{
   "access_token":"my_password",
   "zmq_port":29000,
   "coins":{
      "SAPP":{
         "ticker":"SAPP",
         "name":"Sapphire",
         "rpcuser":"sapprpc",
         "rpcpassword":"sapprpc",
         "rpcport":11111,
         "host":"localhost"
      },
      "DASHD":{
         "ticker":"DASHD",
         "name":"Dashdiamond",
         "rpcuser":"dashdrpc",
         "rpcpassword":"dasdrpc",
         "rpcport":22222,
         "host":"localhost"
      }
   }
}

```

Start a wallet:

```
~/sapp/sapphired -daemon -server
```

Start the project:

```
python3 main.py
```