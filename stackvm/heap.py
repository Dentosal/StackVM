import bisect

class Heap(object):
    def __init__(self):
        self.__values = {}
        self.__sections = []

    def get_at(self, address):
        assert address in self.__values, "Uninitialized memory access"
        return self.__values[address]

    def set_at(self, address, value):
        assert 0 < value < 2**64
        self.__values[address] = value

    def clean_at(self, address):
        del self.__values[address]

    def get_region_at(self, address, count):
        return [self.get_at(a) for a in range(address, address + count)]

    def set_region_at(self, address, values):
        assert all(0 < value < 2**64 for value in values)
        for a, v in zip(range(address, address + len(values)), values):
            self.set_at(a, v)

    def clean_region_at(self, address, count):
        for a in range(address, address + count):
            self.clean_at(a)

    def __reserve(self, start, size):
        bisect.insort_left(self.__sections, (start, size))

    def allocate(self, size):
        """First-free allocator."""
        next_section_start = 0
        for s_start, s_size in self.__sections:
            space_between = s_start - next_section_start
            if space_between >= size:
                self.__reserve(s_start, size)
                return s_start
            next_section_start = s_start + s_size + 1

        # no space between sections, allocate from the end of the memory
        self.__reserve(next_section_start, size)
        return next_section_start

    def resize(self, ptr, newsize):
        # is there enough size to just extend the area?
        for index, (s_start, s_size) in enumerate(self.__sections):
            if s_start == ptr:
                break
        else:
            raise RuntimeError("Invalid pointer passed to Heap.resize")

        inplace = any(
            newsize < s_size, # shinking
            index == len(sections) - 1, # last section
            sections[index + 1][0] - sections[index][0] > newsize # enough space
        )

        if inplace:
            sections[index][1] = newsize
            return ptr
        else:
            del self.__sections[index]
            self.clean_region_at(s_start, s_size)
            newptr = self.alloc(newsize)
            self.set_region_at(newptr, self.get_region_at(ptr, s_size))
            return newptr

    def free(self, ptr):
        for index, (s_start, s_size) in enumerate(self.__sections):
            if s_start == ptr:
                del self.__sections[index]
                self.clean_region_at(s_start, s_size)
                return

        raise RuntimeError("Invalid pointer passed to Heap.free")
