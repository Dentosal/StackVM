class Device(object):
    def write(self, value):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError
