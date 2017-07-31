from more_itertools import chunked

def int_from_bytes(b):
    """Creates integer from little-endian bytes."""
    return int.from_bytes(b, byteorder="little")

def bytes_from_int(v, pad_to):
    """Creates little-endian bytes from integer."""
    assert v >= 0
    return int.to_bytes(v, pad_to, byteorder="little")

def zero_pad_byteint(v, pad_to):
    return bytes_from_int(int_from_bytes(v), pad_to)

def zero_strip_byteint(v):
    return bytes(v).rstrip(b"\x00")

def str_to_u32unicode(data):
    return [zero_pad_byteint(c.encode("utf-8"), 4) for c in data]

def u32unicode_to_str(data):
    return "".join(zero_strip_byteint(b).decode("utf-8") for b in data)

def str_to_u32unicode_bytes(data):
    return b"".join(str_to_u32unicode(data))

def u32unicode_bytes_to_str(data):
    assert len(data) % 4 == 0
    return u32unicode_to_str(chunked(data, 4))

# some unit tests
assert int_from_bytes(bytes([1, 2, 3])) == 0x030201
assert bytes_from_int(0x030201, pad_to=4) == bytes([1, 2, 3, 0])
assert bytes_from_int(0x030201, pad_to=6) == bytes([1, 2, 3, 0, 0, 0])
assert u32unicode_bytes_to_str(str_to_u32unicode_bytes("ääkkönen")) == "ääkkönen"
