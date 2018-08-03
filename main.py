from flask import Flask
from flask import request
from Blockchain import Blockchain
import Utils as Utils
import sys

chain = None
app = Flask(__name__)


@app.route('/')
def index():
    return chain.toJson()


@app.route('/transactions/addList', methods=['POST'])
def addList():
    jsonTs = request.get_json().get('transactions')
    chain.addTransactionsFromJsonList(jsonTs)
    Utils.broadcasttMyBlockchain(chain)
    return str(len(jsonTs)) + " Transaction(s) Added"


@app.route('/receive', methods=['POST'])
def receive():
    global chain
    newChain = Utils.parseFromJson(request.data)
    newTrCount = newChain.transactionsCount()
    currentTrCount = chain.transactionsCount()
    if (newTrCount > currentTrCount):
        if (not newChain.isValid()):
            return "Invalid Blockchain", 400
        chain = newChain
        return "Chain Received", 200
    elif (newTrCount == currentTrCount):
        if (not chain.equal(newChain)):
            return "Invalid Blockchain", 400
        return "Chain Received"
    else:
        return "Chain Is less than current", 400


@app.route('/peers/register', methods=['POST'])
def registerPeer():
    peerData = request.data
    print(peerData)
    print(type(peerData))
    Utils.addPeerFromBroadcast(peerData)
    return "Peer Registered"


@app.route('/peers')
def getPeers():
    return Utils.getPeersAsJson()


port = 5000
if (len(sys.argv) > 1 and sys.argv[1] != "main"):
    port = int(sys.argv[1])
    if (len(sys.argv) > 2 and sys.argv[2] == 'lan'):
        Utils.initializeMyHost(port=port, useLan=True)
    else:
        Utils.initializeMyHost(port=port, useLan=False)
    Utils.loadPeers()
    Utils.broadcastMyHostInfo()
    chain = Utils.getLongestBlockchainFromPeers()
elif (sys.argv[-1] == 'lan'):
    Utils.initializeMyHost(useLan=True)
else:
    Utils.initializeMyHost(useLan=False)
if (chain is None):
    chain = Blockchain()
app.run(port=port)
