from enum import IntEnum
from bobbie.messages import Msg, TOPIC

class TOPIC_Config(IntEnum):
    Zero        = 0
    Get         = 1
    Set         = 2
    Default     = 3
    Save        = 4
    Load        = 5
    Is          = 6

class CONFIG(IntEnum):
    Address          = 0
    LEDAlpha         = 1
    ErrorCooldown    = 2
    ActiveTimeout    = 3
    SerialBridge     = 4


class NodeConfig():
    def __init__(self, node):
        self.node = node
        self.port = node.port

    def set(self, config, value):
        self._send(bytearray(TOPIC_Config.Set))

    def get(self, config, value):
        self._send(bytearray(TOPIC_Config.Get))

    def load(self, config, value):
        self._send(bytearray(TOPIC_Config.Load))

    def save(self, config, value):
        self._send(bytearray(TOPIC_Config.Save))

    def default(self, config, value):
        self._send(bytearray(TOPIC_Config.Default))

    def _send(self, data):
        self.port.send_message( Msg(TOPIC.Config, self.node.address, data ) )
