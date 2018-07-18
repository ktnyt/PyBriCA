class Circuit(object):
    def __init__(self, **components):
        self.components = components
        self.in_ports = []
        self.out_port = None

    def form(self, inputs, output):
        targets = [self.components[key] for key in inputs]
        self.components[output].connect(targets)
        return self

    def expose(self, inputs, output):
        self.in_ports = []
        for key in inputs:
            self.in_ports += self.components[key].in_ports
        self.out_port = self.components[output].out_port
        return self
