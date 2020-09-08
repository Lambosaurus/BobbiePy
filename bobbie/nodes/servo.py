from ..enums import *
from ..node import Node
from ..messages import Msg

class ServoNode(Node):
    def __init__(self, port, address):
        super().__init__(port, address, BoardType.Servo)

    def pulse(self, signals):
        for i in range(0, len(signals), 4):
            msg = Msg(Topic.Servo, self.address, bytearray())
            for servo, pulse_width in signals[i:i+4]:
                s = (servo << 12) | (pulse_width & 0x0FFF)
                msg.write_u16(s)
                self._port.send_message(msg)
        


