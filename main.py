from flask import Flask, render_template, request, redirect, url_for, session
from coinsrpc.BitcoinLike import *
import json

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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
