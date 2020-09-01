from enum import IntEnum
from bobbie.messages import Msg
from bobbie.message_enums import *

class Config(IntEnum):
    Address          = 0
    LEDAlpha         = 1
    ErrorCooldown    = 2
    ActiveTimeout    = 3
    SerialBridge     = 4

class SerialBridge(IntEnum):
    Silent = 0,
    Local = 1,
    All = 2

class NodeConfig():
    def __init__(self, node):
        self.node = node
        self.port = node.port

    def set(self, config, value):
        msg = self._msg(TopicConfig.Set)
        msg.write_u16(config)
        msg.write_u32(value)
        self._send(msg)

    def get(self, config):
        msg = self._msg(TopicConfig.Get)
        msg.write_u16(config)
        self._send(msg)

    def load(self, config, value):
        self._send(self._msg(TopicConfig.Load))

    def save(self, config, value):
        self._send(self._msg(TopicConfig.Save))

    def default(self, config, value):
        self._send(self._msg(TopicConfig.Default))

    def _msg(self, topic):
        return Msg(Topic.Config, self.node.address, bytearray([topic]))

    def _send(self, msg):
        self.port.send_message( msg )
