class Messager(object):
    def __init__(self, init=None):
        self.value = init

    def send(self, value):
        self.value = value

    def recv(self):
        return self.value
