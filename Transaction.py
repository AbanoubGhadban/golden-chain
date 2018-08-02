class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def toString(self):
        return str(self.sender) + " --> " + str(self.receiver) + " (" + str(self.amount) + ")"
