from .operations import Operations

OPS = Operations()

OPCODES = {
    # VM Control
    0x01: OPS.op_exit,

    # Memory access
    0x10: OPS.op_push,
    0x11: OPS.op_load_bytes,
    0x12: OPS.op_load_string,

    0x1A: OPS.op_heap_alloc,
    0x1B: OPS.op_heap_resize,
    0x1C: OPS.op_heap_free,
    0x1D: OPS.op_heap_get_bytes,
    0x1E: OPS.op_heap_set_bytes,

    # Flow control & return stack
    0x20: OPS.op_jmp,
    0x21: OPS.op_jnz,
    0x22: OPS.op_call,
    0x23: OPS.op_return,

    0x2A: OPS.op_to_rs,
    0x2B: OPS.op_from_rs,
    0x2C: OPS.op_fetch_rs,

    # Stack operators
    0x30: OPS.op_drop,
    0x31: OPS.op_dup,
    0x32: OPS.op_swap,
    0x33: OPS.op_rot,
    0x34: OPS.op_over,
    0x34: OPS.op_dupn,

    # Arithmetic operators
    0x40: OPS.op_add,
    0x41: OPS.op_sub,
    0x42: OPS.op_mul,

    # Logical operators
    0x50: OPS.op_not,
    0x51: OPS.op_eq,
    0x52: OPS.op_lt,
    0x53: OPS.op_gt,
    0x54: OPS.op_lte,
    0x55: OPS.op_gte,

    # String processing
    0x60: OPS.op_ucharsz,

    # Debugging
    0x90: OPS.op_print,
    0x91: OPS.op_dbgprint,

    # Device control
    0xD0: OPS.op_dev_write,
    0xD1: OPS.op_dev_read,
}
