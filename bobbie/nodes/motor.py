from ..enums import *
from ..node import Node
from ..messages import Msg
import bobbie.props as props

class MotorNode(Node):
    def __init__(self, port, address):
        super().__init__(port, address, BoardType.Motor)
        self.temperature = props.LiveProperty()
        self.voltage = props.LiveProperty()
        self.current_m1 = props.LiveProperty()
        self.current_m2 = props.LiveProperty()

    def throttle(self, m1, m2):
        msg = Msg(Topic.Motor, self.address, bytearray())
        msg.write_u16(m1)
        msg.write_u16(m2)
        self._port.send_message(msg)

    def _handle_fbk_msg(self, msg):
        if msg.topic == Topic.MotorFbk:
            if len(msg.data) >= 8:
                t = msg.read_i16(0) / 10.0
                v = msg.read_u16(2) / 1000.0
                i1 = msg.read_u16(4) / 1000.0
                i2 = msg.read_u16(6) / 1000.0
                self.temperature._update(t)
                self.voltage._update(v)
                self.current_m1._update(i1)
                self.current_m2._update(i2)

