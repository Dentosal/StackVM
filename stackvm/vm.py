from .image import Image
from .stack import Stack
from .heap import Heap
from .opcodes import OPCODES
from .byteint import *

class MachineState(object):
    def __init__(self, image, **kwargs):
        self._opts = kwargs

        self.image = image
        self.heap = Heap()
        self.data_stack     = Stack(lambda v: 0 <= v < 2**64)
        self.return_stack   = Stack(lambda v: 0 <= v < 2**64)
        self.ip = self.image.start_address

    def pop_next_instruction(self):
        value = self.image.get_at(self.ip, require_executable=True)
        self.ip += 1
        return value

    @property
    def ip_current(self):
        return self.ip - 1

    @property
    def ip_next(self):
        return self.ip

    def step(self):
        value = self.pop_next_instruction()

        assert value in OPCODES, f"Invalid opcode {value}"

        if self._opts.get("debug", False):
            N = 20
            opcode_name = OPCODES[value].__name__[3:]
            top_items = self.data_stack.topn(N + 11)
            top_items = ",".join(f"{x:>4}" for x in top_items[:N]) + (", ..." if len(top_items) > N else "")
            if opcode_name == "push":
                op_arg = str(int_from_bytes(self.image.get_region_at(self.ip_next, 8)))
                print(f"{(f'{opcode_name} ({op_arg})'):<20} | {top_items}")
            else:
                print(f"{opcode_name:<20} | {top_items}")

        if self._opts.get("slow", False):
            import time
            time.sleep(0.2)

        OPCODES[value](self)


def execute_image(image, **kwargs):
    assert isinstance(image, Image)

    ms = MachineState(image, **kwargs)
    while True:
        ms.step()

def main(filename, **kwargs):
    with open(filename, "rb") as f:
        data = f.read()

    execute_image(Image(data), **kwargs)
