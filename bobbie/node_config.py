from enum import IntEnum
from bobbie.messages import *

class TOPIC_Config(IntEnum):
    Get         = 0
    Set         = 1
    Default     = 2
    Save        = 3
    Load        = 4
    Is          = 5

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
        self._send(bytearray([TOPIC_Config.Set]) + WRITE_U16(config) + WRITE_U32(value))

    def get(self, config, value):
        self._send(bytearray([TOPIC_Config.Get]) + WRITE_U16(config))

    def load(self, config, value):
        self._send(bytearray([TOPIC_Config.Load]))

    def save(self, config, value):
        self._send(bytearray([TOPIC_Config.Save]))

    def default(self, config, value):
        self._send(bytearray([TOPIC_Config.Default]))

    def _send(self, data):
        self.port.send_message( Msg(TOPIC.Config, self.node.address, data ) )
