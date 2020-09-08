from enum import IntEnum


class Topic(IntEnum):
    NONE        = 0
    BusState    = 1
    Config      = 2
    State       = 3
    Servo       = 4

class TopicConfig(IntEnum):
    Get         = 0
    Set         = 1
    Default     = 2
    Save        = 3
    Load        = 4
    Is          = 5

class TopicState(IntEnum):
    Request     = 0
    Is          = 1
    Blink       = 2
    Clear       = 3

class State(IntEnum):
	Active      = 0
	Idle        = 1
	Sleep       = 2
	Error       = 3
    
class BoardType(IntEnum):
    Pwr         = 0
    Pi          = 1
    Motor       = 2
    Servo       = 3

class Error(IntEnum):
    NONE              = 0
    BusTimeout        = 1
    DuplicateAddress  = 2
    NoAddress         = 3
    PsuUndervolt      = 4
    PsuOvervolt       = 5
    OverCurrent       = 6