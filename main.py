from coroutine import coroutine
from inspect import signature
from collections import namedtuple


from magma import *


class In:
    def __init__(self, T):
        self.T = T

    def __str__(self):
        return "In"


class Out:
    def __init__(self, T):
        self.T = T

    def __str__(self):
        return "Out"


class Input:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.value = None

    def send(self, value):
        if self.value is not None:
            raise Exception("Input received multiple values in one cycle")
        self.value = value
        self.parent.run_if_inputs_satisfied()


class Output:
    def __init__(self, name):
        self.name = name
        self.outputs = []

        @coroutine
        def co():
            while True:
                curr = yield
                for output in self.outputs:
                    output.send(curr)
        self.co = co()

    def send(self, value):
        self.co.send(value)


class IO:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.outputs = {}
        self.inputs = {}
        for key, value in kwargs.items():
            setattr(self, key, value)
            if isinstance(value, Out):
                self.outputs[key] = value
            elif isinstance(value, In):
                self.inputs[key] = value

    def __str__(self):
        return "IO({})".format(
                    ", ".join("{}={}".format(key, value)
                              for key, value in self.kwargs.items()))


class Coroutine:
    def __init__(self):
        co = coroutine(self.definition)
        self.outputs = [Output(name) for name in self.IO.outputs]
        self.inputs = [Input(name, self) for name in self.IO.inputs]
        self.co = co()
        arg_fields = []
        for name, output in zip(self.IO.outputs, self.outputs):
            setattr(self, name, output)
            arg_fields.append(name)
        for name, input_ in zip(self.IO.inputs, self.inputs):
            setattr(self, name, input_)
            arg_fields.append(name)
        self.args = namedtuple('args', arg_fields)

    def run_if_inputs_satisfied(self):
        for input_ in self.inputs:
            if input_.value is None:
                return
        args = {}
        for input_ in self.inputs:
            args[input_.name] = input_.value
        for output in self.outputs:
            args[output.name] = output
        self.co.send(self.args(**args))
        for input_ in self.inputs:
            input_.value = None


def wire(a, b):
    a.outputs.append(b)


def DefineReg(width=None, init=0):
    if width is None:
        T = Bit
    else:
        T = Bits(width)

    class _Reg(Coroutine):
        IO = IO(
            I = In(T),
            O = Out(T)
        )

        def definition(self):
            value = init
            while True:
                io = yield
                io.O.send(value)
                value = io.I
    return _Reg


class Checker(Coroutine):
    IO = IO(x=In(Bits(4)))

    def __init__(self, expected):
        self.expected = expected
        super().__init__()  # super has to be called after adding fields for
                            # the coroutine to be able to acces them?

    def definition(self):
        while True:
            for e in self.expected:
                io = yield
                assert io.x == e


class Printer(Coroutine):
    IO = IO(x=In(Bits(4)))

    def definition(self):
        while True:
            io = yield
            print(io.x, end=" ")


if __name__ == "__main__":
    inputs = [1, 0, 0, 1, 1, 0, 1, 1, 0]
    expected = [0] + inputs[:-1]
    reg4 = DefineReg(4)()
    checker = Checker(expected)
    printer = Printer()
    wire(reg4.O, checker.x)
    wire(reg4.O, printer.x)
    print("Expected : {}".format(" ".join(str(x) for x in expected)))
    print("Actual   : ", end="")
    for i in inputs:
        reg4.I.send(i)
