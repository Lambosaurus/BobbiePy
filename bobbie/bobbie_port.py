import bobbie.messages as messages

class BobbiePort():
    def __init__(self, port):
        self._open_serialport(port)
        self.parser = messages.MsgParser()

    def _open_serialport(self, port):
        if type(port) == str:
            import serial
            self.port = serial.Serial(port, baudrate=115200)
        else:
            self.port = port
        self.port.timeout = 0

    def poll(self):
        self._read_messages()

    def send_message(self, msg):
        self.port.write(msg.to_bytes())

    def _read_messages(self):
        data = self.port.read(1024)
        for msg in self.parser.parse(data):
            print(msg)
