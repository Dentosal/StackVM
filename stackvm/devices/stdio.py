from ..device import Device
from ..byteutil import *

class StdioDevice(Device):
    VERSION = "1.0.0"

    def write(self, pop_fn):
        count = pop_fn()

        data = bytes(pop_fn() for _ in range(count)).decode("utf-8")
        print(data, end="")

    def read(self, push_fn):
        data = input().encode("utf-8")
        cells = str_to_u32unicode(data.decode("utf-8"))
        for v in reversed(cells):
            push_fn(int_from_bytes(v))

        push_fn(len(cells))
