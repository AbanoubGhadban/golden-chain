from Transaction import Transaction
from Block import Block
import jsonpickle


class Blockchain:
    # smartContract == > code of renting a room in hotel

    def __init__(self, diff=4):
        self.blocks = []
        self.__diff = diff
        block = Block(
            0, [Transaction("Genesis", "Abanoub", 100)], "0"*self.__diff)
        block.mine(self.__diff)
        self.blocks.append(block)

    def blocksCount(self):
        return len(self.blocks)

    def transactionsCount(self):
        count = 0
        for block in self.blocks:
            count += block.transactionsCount()
        return count

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
        block.mine(self.__diff)
        self.blocks.append(block)

    def isValid(self):
        len = self.blocksCount()
        for i in range(len):
            currentBlock = self.blocks[i]
            if (not currentBlock.isMined()):
                return False
            if (i > 0):
                prevBlock = self.blocks[i - 1]
                if (prevBlock.getHash() != currentBlock.previousHash):
                    return False
        return True

    def toString(self):
        chainLen = len(self.blocks)
        data = "\nBlock Size: " + str(chainLen) + "\n"
        data += "*******************************\n"
        for block in self.blocks:
            data += block.toString() + "\n"
            data += "*******************************\n"
        return data

    def addTransactionsFromJsonList(self, jsonTs):
        ts = []
        for jsonTr in jsonTs:
            tr = Transaction.parseFromJsonObject(jsonTr)
            ts.append(tr)
        self.addTransactions(ts)

    def toJson(self):
        return jsonpickle.encode(self)
