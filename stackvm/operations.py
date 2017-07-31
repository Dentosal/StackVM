import operator
from .byteutil import *


class Operations(object):
    @classmethod
    def _simple_un_op(cls, name, op):
        def inner(state):
            a = state.data_stack.pop()
            state.data_stack.push(int(op(a)))
        inner.__name__ = "op_"+name
        setattr(cls, "op_"+name, staticmethod(inner))

    @classmethod
    def _simple_bin_op(cls, name, op):
        def inner(state):
            a = state.data_stack.pop()
            b = state.data_stack.pop()
            state.data_stack.push(int(op(b, a)))
        inner.__name__ = "op_"+name
        setattr(cls, "op_"+name, staticmethod(inner))

    @classmethod
    def _simple_stack_op(cls, name):
        def inner(state):
            getattr(state.data_stack, name)()
        inner.__name__ = "op_"+name
        setattr(cls, "op_"+name, staticmethod(inner))

    def __init__(self):
        self._simple_un_op("not",   lambda a: 1 if a == 0 else 0)

        self._simple_bin_op("add",  lambda b, a: (b + a) % 2**64)
        self._simple_bin_op("sub",  lambda b, a: (2**64 + b - a) % 2**64)
        self._simple_bin_op("mul",  lambda b, a: (b * a) % 2**64)
        self._simple_bin_op("eq",   operator.eq)
        self._simple_bin_op("lt",   operator.lt)
        self._simple_bin_op("gt",   operator.gt)
        self._simple_bin_op("lte",  operator.le)
        self._simple_bin_op("gte",  operator.ge)

        self._simple_stack_op("drop")
        self._simple_stack_op("dup")
        self._simple_stack_op("swap")
        self._simple_stack_op("rot")
        self._simple_stack_op("over")

    @staticmethod
    def op_exit(state):
        exit()

    @staticmethod
    def op_push(state):
        """Pushes u64 value from code stack to data stack."""
        # Pointer is u64 and instructions u8
        value = int_from_bytes(state.pop_next_instruction() for _ in range(8))
        state.data_stack.push(value)

    @staticmethod
    def op_load_bytes(state):
        """Loads N bytes from image, extends them to u64 and pushes to data stack, first value on top."""
        addr = state.data_stack.pop()
        count = state.data_stack.pop()
        for i in reversed(range(addr, addr+count)):
            value = state.image.get_at(i)
            state.data_stack.push(value)

    @staticmethod
    def op_load_string(state):
        """Loads N bytes from image, extends them to u32 unicode scalar values and pushes to stack."""
        addr = state.data_stack.pop()
        count = state.data_stack.pop()
        data = bytes(map(state.image.get_at, range(addr, addr+count)))
        for v in reversed(str_to_u32unicode(data.decode("utf-8"))):
            state.data_stack.push(int_from_bytes(v))

    @staticmethod
    def op_heap_alloc(state):
        size = state.data_stack.pop()
        ptr = state.heap.allocate(size)
        state.data_stack.push(ptr)

    @staticmethod
    def op_heap_resize(state):
        size = state.data_stack.pop()
        ptr = state.data_stack.pop()
        newptr = state.heap.resize(size)
        state.data_stack.push(newptr)

    @staticmethod
    def op_heap_free(state):
        ptr = state.data_stack.pop()
        state.heap.free(size)

    @staticmethod
    def op_heap_get_bytes(state):
        size = state.data_stack.pop()
        ptr = state.data_stack.pop()
        for value in reversed(state.heap.get_region_at(ptr, size)):
            state.data_stack.push(value)

    @staticmethod
    def op_heap_set_bytes(state):
        size = state.data_stack.pop()
        ptr = state.data_stack.pop()
        values = [state.data_stack.pop() for _ in range(size)]
        state.heap.set_region_at(ptr, values)

    @staticmethod
    def op_jmp(state):
        state.ip = state.data_stack.pop()

    @staticmethod
    def op_jnz(state):
        target = state.data_stack.pop()
        if state.data_stack.pop() != 0:
            state.ip = target

    @staticmethod
    def op_call(state):
        state.return_stack.push(state.ip_next)
        state.ip = state.data_stack.pop()

    @staticmethod
    def op_return(state):
        state.ip = state.return_stack.pop()

    @staticmethod
    def op_to_rs(state):
        """Moves a value from the data stack to the return stack."""
        state.return_stack.push(state.data_stack.pop())

    @staticmethod
    def op_from_rs(state):
        """Moves a value from the return stack to the data stack."""
        state.data_stack.push(state.return_stack.pop())

    @staticmethod
    def op_fetch_rs(state):
        """Copies a value from return the stack to the data stack."""
        state.data_stack.push(state.return_stack.pop())

    @staticmethod
    def op_dupn(state):
        """Copies a value from return the stack to the data stack."""
        state.data_stack.dupn(state.data_stack.pop())

    @staticmethod
    def op_ucharsz(state):
        """Stack containing unicode string in"""
        print(state.data_stack.pop())

    @staticmethod
    def op_print(state):
        print(state.data_stack.pop())

    @staticmethod
    def op_dbgprint(state):
        data = []
        count = state.data_stack.pop()

        for _ in range(count):
            data.append(bytes_from_int(state.data_stack.pop(), pad_to=8))

        print(u32unicode_to_str(data), end="")

    @staticmethod
    def op_dev_read(state):
        devcode = state.data_stack.pop()
        dev = state.get_device(devcode)
        dev.read(state.data_stack.push)

    @staticmethod
    def op_dev_write(state):
        devcode = state.data_stack.pop()
        dev = state.get_device(devcode)
        dev.write(state.data_stack.pop)
