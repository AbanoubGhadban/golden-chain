from Transaction import Transaction
from Block import Block
import jsonpickle


class Blockchain:
    # smartContract == > code of renting a room in hotel

    def __init__(self):
        self.blocks = []
        block = Block(0, [Transaction("Genesis", "Abanoub", 100)], "0000")
        block.mine()
        self.blocks.append(block)

    def addTransactions(self, transactions):
        tsLen = len(transactions)
        for i in range(tsLen/2):
            self.__addTransaction(transactions[i*2:i*2+2])

        if (tsLen % 2 == 1):
            self.__addTransaction([transactions[tsLen-1]])

    def __addTransaction(self, ts):
        chainLen = len(self.blocks)
        prevHash = self.blocks[chainLen - 1].getHash()
        block = Block(chainLen, ts, prevHash)
        block.mine()
        self.blocks.append(block)

    def toString(self):
        chainLen = len(self.blocks)
        data = "\nBlock Size: " + str(chainLen) + "\n"
        data += "*******************************\n"
        for block in self.blocks:
            data += block.toString() + "\n"
            data += "*******************************\n"
        return data

    def toJson(self):
        return jsonpickle.encode(self)
