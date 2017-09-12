from magma import *
from silica import *


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
