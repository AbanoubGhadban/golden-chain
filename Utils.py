import hashlib
import jsonpickle
import requests
import socket
from Peer import Peer

LOCAL_HOST = '127.0.0.1'
MAIN_PORT = 5000
peers = []


def initializeMyHost(port=MAIN_PORT, mainHostAddr=LOCAL_HOST, useLan=True):
    global myHost, mainHost
    if (not useLan):
        myHost = Peer(LOCAL_HOST, port)
        mainHost = Peer(mainHostAddr, MAIN_PORT)
    else:
        address = socket.gethostbyname(socket.gethostbyname() + '.local')
        myHost = Peer(address, port)
        mainHost = Peer(mainHostAddr, MAIN_PORT)


def loadPeers():
    global peers
    print(mainHost.getUrl())
    jsonPeers = requests.get(mainHost.getUrl() + '/peers').text
    peers = jsonpickle.decode(jsonPeers)['peers']
    try:
        peers.remove(myHost)
    except ValueError:
        pass
    if (not mainHost in peers):
        peers.append(mainHost)


def broadcastMyHostInfo():
    for peer in peers:
        jsonPeer = jsonpickle.encode({'peer': myHost})
        requests.post(peer.getUrl() + '/peers/register', data=jsonPeer)


def getLongerChain(chain, newChain):
    newTrCount = newChain.transactionsCount()
    currentTrCount = chain.transactionsCount()
    if (newTrCount > currentTrCount):
        return newChain
    else:
        return chain


def getLongestBlockchainFromPeers():
    chain = None
    for peer in peers:
        jsonChain = requests.get(peer.getUrl()).text
        tempChain = jsonpickle.decode(jsonChain)
        if (tempChain.isValid()):
            if (chain is None):
                chain = tempChain
            else:
                chain = getLongerChain(chain, tempChain)
    return chain


def broadcasttMyBlockchain(blockchain):
    jsonChain = jsonpickle.encode(blockchain)
    for peer in peers:
        requests.post(peer.getUrl() + '/receive', data=jsonChain)


def addPeerFromBroadcast(data):
    peer = jsonpickle.decode(data)['peer']
    if ((peer != myHost) and (not peer in peers)):
        peers.append(peer)


def getPeers():
    return peers


def getPeersAsJson():
    return jsonpickle.encode({'peers': peers})


def sha256(data):
    hash_object = hashlib.sha256(data)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def parseFromJson(strData):
    return jsonpickle.decode(strData)
