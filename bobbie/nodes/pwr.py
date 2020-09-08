from ..enums import *
from ..node import Node
from ..messages import Msg

class PwrNode(Node):
    def __init__(self, port, address):
        super().__init__(port, address, BoardType.Pwr)



