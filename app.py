import sys
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, Response
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
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

def is_logged_in():
    if not session:
        return False
    elif session['loggedin']  == True:
        return True
    else:
        return False

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
                '''
                session['loggedin'] = True
                session['user'] = c["rpcuser"]
                session['pass'] = c["rpcpassword"]
                session['host'] = c["host"]
                session['port'] = c["rpcport"]
                session['coin'] = selected_coin
                '''
                additional_claims = {"loggedin": True, "user": c["rpcuser"], "pass": c["rpcpassword"], "host": c["host"], "port": c["rpcport"]}
                access_token = create_access_token(identity=selected_coin, additional_claims=additional_claims)
                print(access_token)
                if pit == "Windows":
                    process = subprocess.Popen(['python.exe', 'wsserver.py', session["coin"]], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python.exe', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                else:
                    process = subprocess.Popen(['python3', 'wsserver.py', session["coin"]], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python3', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                msg = {'success' : 'Connected! You will be redirected in a few seconds...'}
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
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
    return json.dumps(info)

@app.route('/api/getcoins')
def coinslist():
    coins = app_settings["coins"]
    return coins

@app.route('/api/listtxs')
@jwt_required()
def listtxs():
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.listtxs("*", 500)
    for tx in info:
        dt_object = datetime.fromtimestamp(tx["time"])
        tx["time"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/mntotal')
@jwt_required()
def mns():
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''

    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.mncount()
    return json.dumps(info)

@app.route('/api/mymn')
@jwt_required()
def mymns():
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.mymn()
    return json.dumps(info)   

@app.route('/api/mnlist')
@jwt_required()
def masternodeslist():
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.listmn()
    for i in info:
        dt_object = datetime.fromtimestamp(i["lastpaid"])
        i["lastpaid"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/sendtoaddress', methods =['POST'])
@jwt_required()
def sendto():
    '''
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    '''
    msg = ''
    if request.method == 'POST' and 'address' in request.form and 'amount' in request.form and 'passphrase' in request.form:
        coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
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
