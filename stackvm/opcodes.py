from .operations import Operations

OPS = Operations()

OPCODES = {
    0x01: OPS.op_exit,

    0x10: OPS.op_push,
    0x11: OPS.op_load_const,

    0x20: OPS.op_jmp,
    0x21: OPS.op_jnz,
    0x22: OPS.op_call,
    0x23: OPS.op_return,

    0x30: OPS.op_drop,
    0x31: OPS.op_dup,
    0x32: OPS.op_swap,
    0x33: OPS.op_rot,

    0x40: OPS.op_add,
    0x41: OPS.op_sub,
    0x42: OPS.op_mul,

    0x50: OPS.op_not,
    0x51: OPS.op_eq,
    0x52: OPS.op_lt,
    0x53: OPS.op_gt,
    0x54: OPS.op_lte,
    0x55: OPS.op_gte,

    0x98: OPS.op_print_unicode,
    0x99: OPS.op_print,
}
