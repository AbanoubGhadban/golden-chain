import time
from Utils import sha256


class Block:
    def __init__(self, blockNo, tns, prevHash):
        self.blockNo = blockNo
        self.transactions = tns
        self.previousHash = prevHash

        self.pounce = 0
        self.timeStamp = int(time.time())

    def transactionsCount(self):
        return len(self.transactions)

    def toHashableString(self):
        data = "Block No: " + str(self.blockNo) + "\n"
        data += "Previous Hash: " + self.previousHash + "\n"
        data += "Pounce: " + str(self.pounce) + "\n"
        data += "Timestamp: " + str(self.timeStamp) + "\n"

        for ts in self.transactions:
            data += "\n" + ts.toString()
        return data

    def getHash(self):
        return sha256(self.toHashableString())

    def toString(self):
        hashable = self.toHashableString()
        return hashable + "\n\nHash: " + sha256(hashable)

    def mine(self, diff=4):
        while 1 == 1:
            hash = self.getHash()
            if (hash[0:diff] == "0"*diff):
                return
            if (int(time.time()) != self.timeStamp):
                self.timeStamp = int(time.time())
                self.pounce = 0
            else:
                self.pounce += 1

    def isMined(self, diff=4):
        hash = self.getHash()
        return hash[0:diff] == "0"*diff
