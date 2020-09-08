from ..enums import *
from ..node import Node
from ..messages import Msg

class PiNode(Node):
    def __init__(self, port, address):
        super().__init__(port, address, BoardType.Pi)



