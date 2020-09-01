from enum import IntEnum


class Topic(IntEnum):
    Zero        = 0
    BusState    = 1
    Config      = 2
    Hello       = 3

class TopicConfig(IntEnum):
    Get         = 0
    Set         = 1
    Default     = 2
    Save        = 3
    Load        = 4
    Is          = 5

class TopicHello(IntEnum):
    Request     = 0
    Reply       = 1
