from flask import Flask, render_template, request, redirect, url_for, session
from coinsrpc.BitcoinLike import *
from datetime import datetime
import simplejson as json

app = Flask(__name__)
app.secret_key = 'Decenomy2022'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods =['POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'user' in request.form and 'pass' in request.form and 'host' in request.form and 'port' in request.form:
        rpcuser = request.form['user']
        rpcpass = request.form['pass']
        host = request.form['host']
        port = request.form['port']
        try:
            coin =  Decenomy(rpcuser, rpcpass, host, port)
            test_conn = coin.getinfo()
            session['loggedin'] = True
            session['user'] = rpcuser
            session['pass'] = rpcpass
            session['host'] = host
            session['port'] = port
            msg = 'Connected! You will be redirected in a few seconds...'
        except Exception as e:
            msg = str(e)
    elif request.method == 'POST':
        msg = 'Error. All fields are mandatory'
    else:
        msg = 'Error'
    return msg

@app.route('/dash')
def dash():
    coin =  Decenomy(session['user'], session['pass'], session['host'], session['port'])
    info = coin.getinfo()
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
