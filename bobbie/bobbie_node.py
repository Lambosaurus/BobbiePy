from bobbie.node_config import NodeConfig


class BobbieNode():
    def __init__(self, port, address):
        self.address = address
        self.port = port
        self.config = NodeConfig(self)
