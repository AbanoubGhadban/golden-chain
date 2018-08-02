from flask import Flask
from flask import request
from Blockchain import Blockchain
from Utils import parseFromJson

chain = Blockchain()
app = Flask(__name__)


@app.route('/')
def index():
    return chain.toJson()


@app.route('/transactions/addList', methods=['POST'])
def addList():
    jsonTs = request.get_json().get('transactions')
    chain.addTransactionsFromJsonList(jsonTs)
    return str(len(jsonTs)) + " Transaction(s) Added"


@app.route('/receive', methods=['POST'])
def receive():
    global chain
    newChain = parseFromJson(request.data)
    newTrCount = newChain.transactionsCount()
    currentTrCount = chain.transactionsCount()
    if (newTrCount > currentTrCount):
        if (not newChain.isValid()):
            return "Invalid Blockchain", 400
        chain = newChain
        return "Chain Received"
    elif (newTrCount == currentTrCount):
        if (not chain.equal(chain)):
            return "Invalid Blockchain", 400
        return "Chain Received"
    else:
        return "Chain Is less than current", 400
    chain.transactionsCount()


app.run()
