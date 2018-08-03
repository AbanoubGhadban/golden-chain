class Peer:
    def __init__(self, address, port):
        self.setAddress(address)
        self.setPort(port)

    def __eq__(self, other):
        return (
            self.address == other.address and
            self.port == other.port
        )

    def __ne__(self, other):
        return not self == other

    def setAddress(self, address):
        self.address = address

    def setPort(self, port):
        self.port = int(port)

    def getAddress(self):
        return self.address

    def getUrl(self):
        return 'http://' + self.address + ':' + str(self.port)

    def getPort(self):
        return self.port
