class Messager(object):
    def __init__(self, init=None):
        self.value = init
        self.callback = None

    def watch(self, f):
        self.callback = f

    def send(self, value):
        if self.callback: self.callback(value)
        self.value = value

    def recv(self):
        return self.value

