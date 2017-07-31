from .byteutil import *

class Image(object):
    MAGIC   = 0xC0DE3333
    VERSION = 0x00010000
    """
        Image format:

        Little-endian. When an exectable program reads from image, the address
        space starts from the start of the data section, i.e. 16-byte offset.

        field   | size | description
        --------|------|------------
        MAGIC   | u32  | 0xC0DE3333
        VERSION | u32  | MAJOR MINOR PATCH RESERVED
        DATASZ  | u64  | Size of the data section
        DATA    | ...  | Data (r--)
        CODE    | ...  | Code (r-x)

    """

    def __init__(self, rawdata):
        rawdata = bytes(rawdata)

        assert int_from_bytes(rawdata[0:4]) == self.MAGIC, "Incorrect magic number"
        assert int_from_bytes(rawdata[4:8]) == self.VERSION, "TODO: better version check"

        self.__datasz = int_from_bytes(rawdata[8:16])
        self.__values = rawdata[16:]

    def get_at(self, address, require_executable=False):
        assert address < len(self.__values), f"Uninitialized memory access @{address}"
        assert (not require_executable) or address >= self.__datasz
        return self.__values[address]

    def get_region_at(self, address, count, *args):
        return [self.get_at(a, *args) for a in range(address, address + count)]

    @property
    def start_address(self):
        return self.__datasz

    @property
    def raw(self):
        return (
            bytes_from_int(self.MAGIC, pad_to=4) +
            bytes_from_int(self.VERSION, pad_to=4) +
            bytes_from_int(self.__datasz, pad_to=8) +
            self.__values
        )

    def write(self, path):
        with open(path, "wb") as f:
            f.write(self.raw)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            return cls(f.read())

    @classmethod
    def from_sections(cls, data, code):
        return cls(
            bytes_from_int(cls.MAGIC, pad_to=4) +
            bytes_from_int(cls.VERSION, pad_to=4) +
            bytes_from_int(len(data), pad_to=8) +
            bytes(data) +
            bytes(code)
        )
