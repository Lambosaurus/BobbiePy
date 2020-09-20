from ..enums import *
from ..node import Node
from ..messages import Msg
import bobbie.props as props


class ServoNode(Node):
    def __init__(self, port, address):
        super().__init__(port, address, BoardType.Servo)
        self.temperature = props.LiveProperty()
        self.voltage = props.LiveProperty()
        self.current = props.LiveProperty()

    def pulse(self, signals):
        for i in range(0, len(signals), 4):
            msg = Msg(Topic.Servo, self.address, bytearray())
            for servo, pulse_width in signals[i:i+4]:
                s = (servo << 12) | (pulse_width & 0x0FFF)
                msg.write_u16(s)
                self._port.send_message(msg)

    def _handle_fbk_msg(self, msg):
        if msg.topic == Topic.ServoFbk:
            if len(msg.data) >= 6:
                t = msg.read_i16(0) / 10.0
                i = msg.read_u16(2) / 1000.0
                v = msg.read_u16(4) / 1000.0
                self.temperature._update(t)
                self.current._update(i)
                self.voltage._update(v)
        


