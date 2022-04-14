from flask import Flask, render_template, request, redirect, url_for, session
from coinsrpc.BitcoinLike import *
from datetime import datetime
import simplejson as json
import subprocess

app = Flask(__name__)
app.secret_key = 'Decenomy2022'

'''
RPC CONFIG
'''
with open('settings.json') as json_file:
    app_settings = json.load(json_file)



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
                for c in app_settings["coins"]:
                    if c["ticker"] == selected_coin:
                        coin =  Decenomy(c["rpcuser"], c["rpcpassword"], c["host"], c["rpcport"])
                        test_conn = coin.getinfo()
                        session['loggedin'] = True
                        session['user'] = c["rpcuser"]
                        session['pass'] = c["rpcpassword"]
                        session['host'] = c["host"]
                        session['port'] = c["rpcport"]
                        session['coin'] = selected_coin
                        msg = 'Connected! You will be redirected in a few seconds...'
                        break
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
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
    process = subprocess.Popen(['python3', 'wsserver.py', session["coin"]], stdout=None, stderr=None, stdin=None, close_fds=True)
    process = subprocess.Popen(['python3', 'zmq-ws/main.py'], stdout=None, stderr=None, stdin=None, close_fds=True)
    return render_template('dash.html', info=info)

@app.route('/api/listtxs')
def listtxs():
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.listtxs("*", 500)
    for tx in info:
        dt_object = datetime.fromtimestamp(tx["time"])
        tx["time"] = str(dt_object)
    return json.dumps(info)

@app.route('/api/getinfo')
def latestb():
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
    return json.dumps(info)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
