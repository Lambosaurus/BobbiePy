from bobbie.node_config import NodeConfig
import bobbie.messages as msgs


class BobbieNode():
    def __init__(self, port, address):
        self.address = address
        self.port = port
        self.config = NodeConfig(self)

    def remove(self):
        self.port.remove_node(self)

    def handle_msg(self, msg):
        
        if msg.topic == msgs.Topic.Config:
            pass
            

