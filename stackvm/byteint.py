def int_from_bytes(b):
    """Creates integer from little-endian bytes."""
    return sum(v * 0x100**i for i,v in enumerate(b))

def bytes_from_int(v, pad_to=None, exact=True):
    """Creates little-endian bytes from integer."""
    assert v >= 0

    b = bytes()
    while v:
        v, r = divmod(v, 0x100)
        b += bytes([r])

    if pad_to:
        b += bytes((0,) * (pad_to - len(b)))

    if pad_to and exact:
        assert len(b) == pad_to, f"? {pad_to, len(b)}"
    return b


# unit tests
assert int_from_bytes(bytes([1, 2, 3])) == 0x030201
assert bytes_from_int(0x030201) == bytes([1, 2, 3])
assert bytes_from_int(0x030201, pad_to=2, exact=False) == bytes([1, 2, 3])
assert bytes_from_int(0x030201, pad_to=4) == bytes([1, 2, 3, 0])
assert bytes_from_int(0x030201, pad_to=6) == bytes([1, 2, 3, 0, 0, 0])
