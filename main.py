from flask import Flask
from flask import request
from Blockchain import Blockchain

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


app.run()
