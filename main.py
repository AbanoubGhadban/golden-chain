from flask import Flask
from Blockchain import Blockchain

chain = Blockchain()
app = Flask(__name__)


@app.route('/')
def index():
    return chain.toJson()


app.run()
