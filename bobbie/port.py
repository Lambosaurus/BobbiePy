import time

from bobbie.messages import MsgParser, Msg
from bobbie.node import Node
from bobbie.enums import *


class Promise():
    def __init__(self, port, timeout):
        self.value = None
        self.is_complete = False
        self.__end_time = timeout + time.time()
        self.__port = port
        self.__callbacks = []
        self.__mutation = None

    def _mutate(self, mutation):
        self.__mutation = mutation

    def _set(self, value):
        self.__resolve(value)

    def _update(self, t):
        if t > self.__end_time:
            self.__resolve(None)

    def __resolve(self, value):
        if self.__mutation:
            value = self.__mutation(value)
        self.value = value
        self.is_complete = True
        for callback in self.__callbacks:
            callback(value)
        self.__port._remove_promise(self)

    def wait(self):
        while not self.done:
            time.sleep(0.01)
            self.__port.poll()
        return self.value

    def callback(self, callback):
        self.__callbacks.append(callback)


class Bobbie():
    def __init__(self, port):
        self.__open_serialport(port)
        self.__parser = MsgParser()
        self.nodes = {}
        self.broadcast_node = Node.create(self, 0, None)
        self.immediate_node = Node.create(self, -1, None)
        self._promises = {}

    def create_node(self, address, board):
        node = Node.create(self, address, board)
        self.nodes[address] = node
        return node

    def remove_node(self, node):
        node.__port = None
        if node.address in self.nodes:
            self.nodes.pop(node.address)

    def discover_nodes(self, timeout = 0.5):
        msg = Msg(Topic.State, 0, bytearray([TopicState.Request]))
        self.send_message(msg)
        promise = self._create_promise(timeout)
        promise._mutate(lambda v: list(self.nodes.values()) )
        return promise

    def __open_serialport(self, port):
        if type(port) == str:
            import serial
            self.__port = serial.Serial(port, baudrate=115200)
        else:
            self.__port = port
        self.__port.timeout = 0

    def poll(self):
        self.__read_messages()
        self.__update_promises()

    def wait_for_promises(self):
        while len(self._promises):
            time.sleep(0.01)
            self.poll()

    def send_message(self, msg):
        self.__port.write(msg.to_bytes())

    def __read_messages(self):
        data = self.__port.read(1024)
        for msg in self.__parser.parse(data):
            if msg.src in self.nodes:
                self.nodes[msg.src]._handle_msg(msg)
            elif msg.src > 0 and msg.topic == Topic.State:
                self.__handle_new_node_state(msg)

    def __handle_new_node_state(self, msg):
        if len(msg.data) >= 5 and msg.data[0] == TopicState.Is:
            self.create_node(msg.src, BoardType(msg.data[1]))
            self.nodes[msg.src]._handle_msg(msg)

    def __update_promises(self):
        t = time.time()
        for promise in list(self._promises.values()):
            promise._update(t)

    def _create_promise(self, timeout):
        promise = Promise(self, timeout)
        self._promises[promise] = promise
        return promise

    def _remove_promise(self, promise):
        self._promises.pop(promise)
