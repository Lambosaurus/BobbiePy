from bobbie.enums import Topic

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
    def __init__(self, topic, dst, data):
        self.topic = topic
        self.src = 0
        self.dst = dst
        self.data = data

    @staticmethod
    def from_bytes(bfr, size):
        header = bfr[1]
        topic = ((header & HEADER_MASK_TOPIC) << 2) | bfr[2]
        msg = Msg(topic, 0, bfr[SERIAL_SIZE_HEADER:size])
        msg.src = bfr[3]
        return msg

    def to_bytes(self):
        length = len(self.data)
        if length > SERIAL_SIZE_DATA:
            raise Exception("Data len cannot be greater than {}".format(SERIAL_SIZE_DATA))

        header = ((self.topic >> 2) & HEADER_MASK_TOPIC) | length
        if self.dst < 0:
            self.dst = 0
            header |= SERIAL_FLAG_TOLOCAL
        return bytearray([
            SERIAL_START_CHAR,
            header,
            self.topic & 0xFF,
            self.dst,
            ]) + self.data

    def __repr__(self):
        topic = Topic(self.topic).name
        return "<{}: src={}, {}>".format(topic, self.src, self.data.hex())

    def write_u8(self, value):
        self.data.append(value)

    def write_u16(self, value):
        self.data += bytearray([
            0xFF & (value >> 8),
            0xFF & (value),
        ])

    def write_u32(self, value):
        self.data += bytearray([
            0xFF & (value >> 24),
            0xFF & (value >> 16),
            0xFF & (value >> 8),
            0xFF & (value),
        ])

    def read_u8(self, i):
        return self.data[i]

    def read_i8(self, i):
        u8 = self.read_u8(i)
        return u8 - 0x100 if u8 & 0x80 else u8

    def read_u16(self, i):
        return (self.data[i] << 8) | self.data[i+1]

    def read_i16(self, i):
        u16 = self.read_u16(i)
        return u16 - 0x10000 if u16 & 0x8000 else u16

    def read_u32(self, i):
        return (self.data[i] << 24) | (self.data[i+1] << 16) | (self.data[i+2] << 8) | self.data[i+3]

class MsgParser():
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
