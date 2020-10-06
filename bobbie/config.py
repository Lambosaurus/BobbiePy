from enum import IntEnum
from bobbie.messages import Msg
from bobbie.enums import *
from bobbie.props import LiveProperty

class Config(IntEnum):
    Address          = 0
    LEDAlpha         = 1
    ErrorCooldown    = 2
    ActiveTimeout    = 3
    SerialBridge     = 4
    TempLimit        = 5
    FeedbackIdle     = 6
    FeedbackActive   = 7
    COUNT            = 8

class SerialBridge(IntEnum):
    Silent = 0,
    Local = 1,
    All = 2

class ConfigProperty(LiveProperty):
    def __init__(self, config, id):
        super().__init__(self)
        self.__config = config
        self.__id = id

    def set(self, value):
        pass

    def get(self):
        pass

class NodeConfig():
    def __init__(self, node):
        self.node = node
        self.port = node._port
        self.__props = []
        for _ in range(Config.COUNT):
            self.__props.append(LiveProperty())


    def set(self, config, value):
        msg = self.__msg(TopicConfig.Set)
        msg.write_u16(config)
        msg.write_u32(value)
        self.__send(msg)

    def get(self, config):
        msg = self.__msg(TopicConfig.Get)
        msg.write_u16(config)
        self.__send(msg)

    def load(self, config, value):
        self.__send(self.__msg(TopicConfig.Load))

    def save(self, config, value):
        self.__send(self.__msg(TopicConfig.Save))

    def default(self, config, value):
        self.__send(self.__msg(TopicConfig.Default))

    def _handle_msg(self, msg):
        pass

    def __msg(self, topic):
        return Msg(Topic.Config, self.node.address, bytearray([topic]))

    def __send(self, msg):
        self.port.send_message( msg )
