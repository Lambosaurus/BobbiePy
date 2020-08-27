
class TOPIC():
    Zero        = 0
	BusState    = 1
	Config      = 2

# These constants mimic the C conventions by choice.
SERIAL_START_CHAR     = 0x5F
SERIAL_SIZE_HEADER	  = 4
SERIAL_SIZE_DATA	  = 8
SERIAL_SIZE_MAX	      = SERIAL_SIZE_HEADER + SERIAL_SIZE_DATA

HEADER_MASK_LEN		  = 0x0F
HEADER_MASK_TOPIC	  = 0xC0
HEADER_MASK_FLAGS	  = 0x30
SERIAL_FLAG_TOLOCAL	  = 0x10

class Msg():
    def __init__(self, topic, src, dst, data):
        self.topic = topic
        self.src = src
        self.dst = dst
        self.data = data
        self.len = len(data)
        self.to_local = false

        if (self.len > SERIAL_SIZE_DATA):
            raise Exception("Data len cannot be greater than {}".format(SERIAL_SIZE_DATA))

    @staticmethod
    def create(topic, dst, data=bytearray()):
        if type(data) != bytearray:
            data = bytearray(data)
        return Msg(topic, 0, dst, data)

    @staticmethod
    def from_bytes(bfr, size):
        header = bfr[1]
        topic = ((header & HEADER_MASK_TOPIC) << 2) | bfr[2]
        src = bfr[3]
        return Msg(topic, 0, dst, bfr[SERIAL_SIZE_HEADER:length])

    def to_bytes(self):
        header = ((self.topic >> 2) & HEADER_MASK_TOPIC) | self.len
        if self.to_local:
            heade |= SERIAL_FLAG_TOLOCAL
        return bytearray([
            SERIAL_START_CHAR,
            header,
            self.topic & 0xFF,
            self.dst,
            ]) + self.data

class MsgParser()
    def __init__(self):
        self.bfr = bytearray(SERIAL_SIZE_MAX)
        self.index = 0
        self.length = 0

    def parse(self, data):

        for ch in data:
            if self.index == 0:
                if ch == SERIAL_START_CHAR:
                    self.bfr[0] = ch
                    self.index = 1
            
            elif self.index == 1:
                dlen = ch & HEADER_MASK_LEN
                if dlen > SERIAL_SIZE_DATA:
                    self.index = 0
                else:
                    self.bfr[1] = ch
                    self.index = 2
                    self.length = dlen + SERIAL_SIZE_HEADER
            
            else:
                self.bfr[self.index] = ch
                self.index += 1
                if self.index >= self.length:
                    self.index = 0
                    yield Msg.from_bytes(self.bfr, self.length)
                    
        return
