from flask import Flask, render_template, request, redirect, url_for, session, Response
from coinsrpc.BitcoinLike import *
from datetime import datetime
from dswutils.bootstrap import *
import sys, io
import simplejson as json
import subprocess
import requests
import platform

app = Flask(__name__)
app.secret_key = 'Decenomy2022'

'''
RPC CONFIG
'''
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

@app.route('/')
def index():
    return render_template('index.html', app_settings=app_settings)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user', None)
    session.pop('pass', None)
    session.pop('host', None)
    session.pop('port', None)
    session.pop('coin', None)
    return redirect(url_for('index'))

@app.route('/login', methods =['POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'password' in request.form:
        app_pass = request.form["password"]
        selected_coin = request.form.get("coinselect")
        if app_pass == app_settings["access_token"]:
            try:
                c = app_settings["coins"][selected_coin]
                print(c)
                coin =  Decenomy(c["rpcuser"], c["rpcpassword"], c["host"], c["rpcport"])
                test_conn = coin.getinfo()
                session['loggedin'] = True
                session['user'] = c["rpcuser"]
                session['pass'] = c["rpcpassword"]
                session['host'] = c["host"]
                session['port'] = c["rpcport"]
                session['coin'] = selected_coin
                if pit == "Windows":
                    process = subprocess.Popen(['python.exe', 'wsserver.py', session["coin"]], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python.exe', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                else:
                    process = subprocess.Popen(['python3', 'wsserver.py', session["coin"]], stdout=None, stderr=None, stdin=None, close_fds=True)
                    process2 = subprocess.Popen(['python3', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
                msg = 'Connected! You will be redirected in a few seconds...'
            except Exception as e:
                msg = str(e)
        else:
            msg = 'Error, incorrect password'
    elif request.method == 'POST':
        msg = 'Error. All fields are mandatory'
    else:
        msg = 'Error'
    return msg

@app.route('/dash')
def dash():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
    mn = coin.mncount()
    mynodes = len(coin.mymn())
    price = requests.get("https://explorer.decenomy.net/coreapi/v1/coins/" + session["coin"] + "/pairs/EUR?param=bid").json()
    p = round(price["response"]["rate"], 3)
    priceb = requests.get("https://explorer.decenomy.net/coreapi/v1/coins/" + session["coin"] + "/pairs/BTC?param=bid").json()
    pb = round(priceb["response"]["rate"], 8)

    return render_template('dash.html', info=info, mn=mn, mynodes=mynodes, p=p, pb=pb)

@app.route('/receive')
def receive():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    addr = coin.getnewaddr()
    return render_template('receive.html', addr=addr)

@app.route('/send')
def send():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    return render_template('send.html')

@app.route('/mnexplorer')
def mnexplorer():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    return render_template('mnexplorer.html')

@app.route('/mymn')
def listmymn():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    return render_template('mymn.html')

@app.route('/bootstrap')
def boot():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    coin.s()
    return render_template('bootstrap.html')

@app.route('/bootstraplog')
def progress():
    if is_logged_in() == False:
        return redirect(url_for('index'))
    coin = session['coin']
    c = app_settings["coins"][coin]
    coin_name = c["name"].lower()
    def getstatus():
        yield "data:Downloading bootstrap... Please wait..\n\n"
        bdownload("https://explorer.decenomy.net/bootstraps/"+coin+"/bootstrap.zip", "bootstrap.zip")
        yield "data:Extracting....\n\n"
        wipe(coin_name)
        yield "data:Done! Please restart your wallet\n\n"
    return Response(getstatus(), mimetype='text/event-stream')

@app.route('/api/listtxs')
def listtxs():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.listtxs("*", 500)
    for tx in info:
        dt_object = datetime.fromtimestamp(tx["time"])
        tx["time"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/getinfo')
def latestb():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
    return json.dumps(info)

@app.route('/api/mntotal')
def mns():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.mncount()
    return json.dumps(info)

@app.route('/api/mymn')
def mymns():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.mymn()
    return json.dumps(info)   

@app.route('/api/mnlist')
def masternodeslist():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.listmn()
    for i in info:
        dt_object = datetime.fromtimestamp(i["lastpaid"])
        i["lastpaid"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/sendtoaddress', methods =['POST'])
def sendto():
    if is_logged_in() == False:
        return json.dumps({"error":"Unauthorized"})
    msg = ''
    if request.method == 'POST' and 'address' in request.form and 'amount' in request.form and 'passphrase' in request.form:
        coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
        valid = coin.validate(request.form["address"])
        if valid["isvalid"] == True:
            try:
                unlock = coin.unlock(request.form["passphrase"], 5)
                txid = coin.send(request.form["address"], request.form["amount"])
                msg = "Success! Transaction id: " + txid
            except Exception as e:
                msg = str(e)
        else:
            msg = "Invalid address"
    else:
        msg = "All fields are mandatory"
    return msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
