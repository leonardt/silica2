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


class Expected(Coroutine):
    IO = IO(O = Out(Bits(4)))

    def __init__(self, expected):
        self.expected = expected
        super().__init__()  # super has to be called after adding fields for
                            # the coroutine to be able to acces them because
                            # the coroutine is initialized during the super

    def definition(self):
        while True:
            for value in self.expected:
                io = yield
                io.O.send(value)


class Checker(Coroutine):
    IO = IO(actual=In(Bits(4)),
            expected=In(Bits(4)))

    def definition(self):
        while True:
            io = yield
            assert io.actual == io.expected


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
    expected_co = Expected(expected)
    checker = Checker()
    printer = Printer()
    wire(reg4.O, checker.actual)
    wire(expected_co.O, checker.expected)
    wire(reg4.O, printer.x)
    print("Expected : {}".format(" ".join(str(x) for x in expected)))
    print("Actual   : ", end="")
    for i in inputs:
        reg4.I.send(i)
        next(expected_co)
