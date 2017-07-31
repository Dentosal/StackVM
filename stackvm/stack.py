class Stack(object):
    def __init__(self, checker=None):
        self.__stack = []
        self.__checker = checker

    @property
    def depth(self):
        return len(self.__stack)

    @property
    def empty(self):
        return self.depth == 0

    @property
    def top(self):
        return self.__stack[0]

    def topn(self, n):
        return self.__stack[-n:][::-1]

    # primitives

    def push(self, item):
        assert self.__checker is None or self.__checker(item)
        self.__stack.append(item)

    def pop(self):
        assert not self.empty
        return self.__stack.pop()

    def pick(self, n):
        assert self.depth > n
        self.push(self.__stack[-n-1])

    def roll(self, n):
        assert self.depth > n
        self.push(self.__stack.pop(-n-1))

    # utilities

    def drop(self):
        self.pop()

    def dup(self):
        self.pick(0)

    def dupn(self, n):
        assert n >= 1
        for _ in range(n):
            self.pick(n - 1)

    def over(self):
        self.pick(1)

    def swap(self):
        self.roll(1)

    def rot(self):
        self.roll(2)
