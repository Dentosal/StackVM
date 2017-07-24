import operator
from .byteint import *


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
    def op_load_const(state):
        """Loads N bytes from image, extends them to u64 and pushes to data stack."""
        addr = state.data_stack.pop()
        count = state.data_stack.pop()
        for i in range(addr, addr+count):
            value = state.image.get_at(i)
            state.data_stack.push(value)

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
    def op_print(state):
        print(state.data_stack.pop())

    @staticmethod
    def op_print_unicode(state):
        data = []
        count = state.data_stack.pop()

        for _ in range(count):
            data.append(state.data_stack.pop())

        print(bytes(data[::-1]).decode("utf-8"), end="")
