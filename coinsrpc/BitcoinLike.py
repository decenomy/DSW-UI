from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time

class Bitcoin:
    def __init__(self, rpcuser, rpcpassword, host, port):
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.host = host
        self.port = port
        self.rpc = AuthServiceProxy("http://%s:%s@%s:%s"%(self.rpcuser, self.rpcpassword, self.host, self.port))
    def getinfo(self):
        getinfo = self.rpc.getinfo()
        return getinfo
    def peer(self):
        peer = self.rpc.getpeerinfo()
        return peer
    def listtxs(self, account, number):
        list = self.rpc.listtransactions(account, number)
        return list
    def gettx(self, txid):
        tx = self.rpc.gettransaction(txid)
        return tx
    def balance(self):
        bal = self.rpc.getbalance()
        return bal
    def unlock(self, passphrase, time):
        res = self.rpc.walletpassphrase(passphrase, time)
        return res
    def send(self, address, amount):
        txid = self.rpc.sendtoaddress(address, amount)
        return txid
    def blocks(self):
        bal = self.rpc.getblockcount()
        return bal
    def hash(self, block):
        bal = self.rpc.getblockhash(block)
        return bal
