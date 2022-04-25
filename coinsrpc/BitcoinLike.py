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
    def block(self, block):
        block_info = self.rpc.getblock(block)
        return block_info
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
    def listunspent(self, addr, minc = 1, maxc = 9999999, watch = 1,):
        txs_list = self.rpc.listunspent(minc, maxc, addr, watch)
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
    def mnoutputs(self):
        info = self.rpc.getmasternodeoutputs()
        return info   
    def listmn(self, f=""):
        mn = self.rpc.listmasternodes(f)  
        return mn  
    def setsplit(self, amount):
        try:
            result = self.rpc.setstakesplitthreshold(amount)
            r = True
        except:
            r = False
        return r
    def mnkey(self):
        key = self.rpc.createmasternodekey()
        return key 
    def dumpkey(self, address):
        privkey = self.rpc.dumpprivkey(address)
        return privkey 
    def dumpw(self, filename):
        try:
            result = self.rpc.dumpwallet(filename)
            r = True
        except:
            r = False
        return r 
    def encryptw(self, walletpassphrase):
        try:
            result = self.rpc.encryptwallet(walletpassphrase) 
            r = True
        except:
            r = False
        return r 
    def changepw(self, oldpw, newpw):
        try:
            result = self.rpc.walletpassphrasechange(oldpw, newpw) 
            r = True
        except:
            r = False
        return r
    def importkey(self, privkey, label="", rescan=True):
        try:
            result = self.rpc.importprivkey(privkey, label, rescan)
            r = True
        except:
            r = False
        return r 
    def send_many(self, addresses, conf=1, comment="", dummy=""):
        txid = self.rpc.sendmany(dummy, addresses, conf, comment)
        return txid
    def addrbylabel(self, label):
        addresses = self.rpc.getaddressesbylabel(label)
        return addresses
    def mns(self, mode):
        mnlist = self.rpc.mnsync(mode)
        return mnlist
    def mncount(self):
        mnc = self.rpc.getmasternodecount()
        return mnc
    def mnwinner(self, block=10, f=""):
        mnw = self.rpc.getmasternodewinners(block, f)
        return mnw
    def s(self):
        mnw = self.rpc.stop()
        return True

