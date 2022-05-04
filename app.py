import sys
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, Response
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from coinsrpc.BitcoinLike import *
from datetime import datetime
from dswutils.bootstrap import *
import io
import simplejson as json
import subprocess
import requests
import platform

"""
---------------------- SETTINGS AND FUNCTIONS -----------------------
"""

app = Flask(__name__)
app.secret_key = 'Decenomy2022'
app_config = {"host": "0.0.0.0", "port": sys.argv[1]}
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

with open('settings.json') as json_file:
    app_settings = json.load(json_file)

pit = platform.system()


"""
---------------------- DEVELOPER MODE CONFIG -----------------------
"""
# Developer mode uses app.py
if "app.py" in sys.argv[0]:
  # Update app config
  app_config["debug"] = True

  # CORS settings
  cors = CORS(
    app,
    resources={r"/*": {"origins": "http://localhost*"}},
  )

  # CORS headers
  app.config["CORS_HEADERS"] = "Content-Type"


"""
--------------------------- REST CALLS -----------------------------
"""

@app.route('/login', methods =['POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'password' in request.json and 'coin' in request.json:
        app_pass = request.json["password"]
        selected_coin = request.json["coin"]
        if app_pass == app_settings["access_token"]:
            try:
                c = app_settings["coins"][selected_coin]
                coin =  Decenomy(c["rpcuser"], c["rpcpassword"], c["host"], c["rpcport"])
                test_conn = coin.getinfo()
                additional_claims = {"loggedin": True, "user": c["rpcuser"], "pass": c["rpcpassword"], "host": c["host"], "port": c["rpcport"]}
                access_token = create_access_token(identity=c["ticker"], additional_claims=additional_claims)
                if pit == "Windows":
                    process = subprocess.Popen(['python.exe', 'wsserver.py', selected_coin], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python.exe', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                else:
                    process = subprocess.Popen(['python', 'wsserver.py', selected_coin], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                msg = {'success' : 'Connected! You will be redirected in a few seconds...', 'token': access_token}
            except Exception as e:
                msg = {'error': str(e) }
        else:
            msg = {'error': 'incorrect password'}
    elif request.method == 'POST':
        msg = {'error' : 'All fields are mandatory'}
    else:
        msg = {'error' : 'Invalid request'}
    return json.dumps(msg)

@app.route('/api/getinfo')
@jwt_required()
def latestb():
    user_rpc = get_jwt()
    coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
    info = coin.getinfo()
    return json.dumps(info)

@app.route('/api/getcoins')
def coinslist():
    coins = app_settings["coins"]
    return coins

@app.route('/api/listtxs')
@jwt_required()
def listtxs():
    user_rpc = get_jwt()
    coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
    info = coin.listtxs("*", 500)
    for tx in info:
        dt_object = datetime.fromtimestamp(tx["time"])
        tx["time"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/mntotal')
@jwt_required()
def mns():
    user_rpc = get_jwt()
    coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
    info = coin.mncount()
    return json.dumps(info)

@app.route('/api/mymn')
@jwt_required()
def mymns():
    user_rpc = get_jwt()
    coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
    info = coin.mymn()
    return json.dumps(info) 

@app.route('/api/price')
@jwt_required()
def price():
    current_coin = get_jwt_identity()
    try:
        price = requests.get("https://explorer.decenomy.net/coreapi/v1/coins/" + current_coin + "/pairs/EUR?param=bid").json()
        p = round(price["response"]["rate"], 3)
        priceb = requests.get("https://explorer.decenomy.net/coreapi/v1/coins/" + current_coin + "/pairs/BTC?param=bid").json()
        pb = round(priceb["response"]["rate"], 8)
    except:
        p = 0
        pb = 0
    price_info = {"coin": current_coin, "eur": p, "btc": pb}
    
    return json.dumps(price_info)   

@app.route('/api/mnlist')
@jwt_required()
def masternodeslist():
    user_rpc = get_jwt()
    coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
    info = coin.listmn()
    for i in info:
        dt_object = datetime.fromtimestamp(i["lastpaid"])
        i["lastpaid"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/sendtoaddress', methods =['POST'])
@jwt_required()
def sendto():
    msg = ''
    if request.method == 'POST' and 'address' in request.form and 'amount' in request.form and 'passphrase' in request.form:
        user_rpc = get_jwt()
        coin =  Decenomy(user_rpc['user'], user_rpc['pass'], user_rpc['host'], user_rpc['port'])
        valid = coin.validate(request.form["address"])
        if valid["isvalid"] == True:
            try:
                unlock = coin.unlock(request.form["passphrase"], 5)
                txid = coin.send(request.form["address"], request.form["amount"])
                msg = {"success" : "Transaction id: " + txid }
            except Exception as e:
                msg = str(e)
        else:
            msg = {"error":"Invalid address"}
    else:
        msg = {"error":"All fields are mandatory"}
    return json.dumps(msg)

"""
-------------------------- APP SERVICES ----------------------------
"""
# Quits Flask on Electron exit
@app.route("/quit")
def quit():
  shutdown = request.environ.get("werkzeug.server.shutdown")
  shutdown()
  return


if __name__ == "__main__":
  app.run(**app_config)
