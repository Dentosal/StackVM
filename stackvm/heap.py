class Heap(object):
    def __init__(self):
        self.__values = {}

    def get_at(self, address):
        assert address in self.__values, "Uninitialized memory access"
        return self.__values[address]

    def set_at(self, address, value):
        assert 0 < value < 2**64
        self.__values[address] = value

    def get_region_at(self, address, count):
        return [self.get_at(a) for a in range(address, address + count)]

    def set_region_at(self, address, values):
        assert all(0 < value < 2**64 for value in values)
        for a, v in zip(range(address, address + len(values)), values):
            self.set_at(a, v)
