from ..enums import BoardType
from ..node import Node

from .servo import ServoNode
from .pi import PiNode
from .pwr import PwrNode
from .motor import MotorNode

__NODE_TYPES = {
    BoardType.Pwr:      PwrNode,
    BoardType.Pi:       PiNode,
    BoardType.Motor:    MotorNode,
    BoardType.Servo:    ServoNode,
}

def _create_node(port, address, board):
    if board in __NODE_TYPES:
        return __NODE_TYPES[board](port, address)
    return Node(port, address, board)