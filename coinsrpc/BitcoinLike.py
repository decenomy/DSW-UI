from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time

class Decenomy:
    def __init__(self, rpcuser, rpcpassword, host, port):
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.host = host
        self.port = port
        self.rpc = AuthServiceProxy("http://%s:%s@%s:%s"%(self.rpcuser, self.rpcpassword, self.host, self.port))
    #== Blockchain ==#
    def blocks(self):
        num_blocks = self.rpc.getblockcount()
        return num_blocks
    def hash(self, block):
        block_hash = self.rpc.getblockhash(block)
        return block_hash
    def getblockchaininfo():
        info = self.rpc.getblockchaininfo()
        return info
    #== Network ==#
    def addnode(self, node, method):
        try:
            res = self.rpc.addnode(node, method)
            a = True
        except:
            a = False
        return a
    def clearbanned(self):
        res = self.rpc.clearbanned()
        return res
    #== Control ==#
    def getinfo(self):
        getinfo = self.rpc.getinfo()
        return getinfo
    #== Util ==#
    def validate(self, address):
        res = self.rpc.validateaddress(address)
        return res
    #== Wallet ==#
    def getnewaddr(self, label = ""):
        addr  = self.rpc.getnewaddress(label)
        return addr
    def staking(self):
        status = self.rpc.getstakingstatus()
        return status
    def peers(self):
        peers_list = self.rpc.getpeerinfo()
        return peer_list
    def listtxs(self, account, number):
        txs_list = self.rpc.listtransactions(account, number)
        return txs_list
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