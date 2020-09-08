from bobbie.config import NodeConfig
from bobbie.messages import Msg
from bobbie.enums import *
import bobbie.props as props

class Node():
    def __init__(self, port, address, board):
        self.address = address
        self._port = port
        self.config = NodeConfig(self)
        self.state = props.LiveProperty()
        self.error = props.LiveProperty()
        self.board = board

    @staticmethod
    def create(port, address, board):
        return Node(port, address, board)

    def check_exists(self, timeout = 0.5):
        msg = Msg(Topic.State, self.address, bytearray([
            TopicState.Request
        ]))
        self._port.send_message(msg)
        promise = self._port._create_promise(timeout)
        promise._mutate(lambda v: v != None)
        self.state.subscribe(promise._set)
        promise.callback(lambda v: self.state.unsubscribe(promise._set))
        return promise

    def clear_error(self):
        msg = Msg(Topic.State, self.address, bytearray([TopicState.Clear]))
        self._port.send_message(msg)

    def remove(self):
        self._port.remove_node(self)

    def _handle_msg(self, msg):
        if msg.topic == Topic.Config:
            self.config._handle_msg(msg)
        elif msg.topic == Topic.State:
            self.__handle_state(msg)

    def __handle_state(self, msg):
        if len(msg.data) >= 5 and msg.data[0] == TopicState.Is:
            self.state._update(State(msg.data[2]))
            self.error._update(Error(msg.read_u16(3)))

    def blink(self, color=(0,128,255), period=500, counts=2 ):
        msg = Msg(Topic.State, self.address, bytearray([
            TopicState.Blink,
            color[0],
            color[1],
            color[2]
        ]))
        msg.write_u16(period)
        msg.write_u8(counts)
        self._port.send_message(msg)

    def __repr__(self):
        return "<Node: {}, {}>".format(self.address, str(self.board))

