class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    @staticmethod
    def parseFromJsonObject(jsonTr):
        sender = jsonTr.get("sender")
        receiver = jsonTr.get("receiver")
        amount = jsonTr.get("amount")
        return Transaction(sender, receiver, amount)

    def toString(self):
        return str(self.sender) + " --> " + str(self.receiver) + " (" + str(self.amount) + ")"

    def equal(self, transaction):
        return (
            self.sender == transaction.sender and
            self.receiver == transaction.receiver and
            self.amount == transaction.amount
        )
