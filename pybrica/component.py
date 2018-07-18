try:
    from inspect import signature, Signature, Parameter
except:
    from funcsigs import signature, Signature, Parameter

from pybrica import messager

class Component(object):
    def __init__(self, f, interval=1000, offset=0, sleep=0):
        assert(interval > 0)
        assert(offset >= 0)
        assert(sleep >= 0)

        self.f = f

        self.interval = interval
        self.offset = offset
        self.sleep = sleep

        self.inputs = []
        self.output = None

        self.in_ports = []
        self.out_port = None

        sig = signature(f)

        for _, param in sig.parameters.items():
            if param.default is not Parameter.empty:
                default = param.default
            elif param.annotation is not Parameter.empty:
                default = param.annotation()
            else:
                default = None

            self.in_ports.append(messager.Messager(default))
            self.inputs.append(default)

        if sig.return_annotation is not Signature.empty:
            default = sig.return_annotation()
        else:
            default = None

        self.out_port = messager.Messager(default)
        self.output = default

    def collect_input(self):
        for i, source in enumerate(self.in_ports):
            self.inputs[i] = source.recv()

    def expose_output(self):
        self.out_port.send(self.output)
        self.output = None

    def connect(self, targets):
        assert(len(targets) == len(self.in_ports))
        for i, target in enumerate(targets):
            self.in_ports[i] = target.out_port

    def fire(self):
        self.output = self.f(*self.inputs)

    def __call__(self, *targets):
        self.connect(targets)
        return self
