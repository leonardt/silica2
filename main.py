from coroutine import coroutine
from inspect import signature


class Output:
    def __init__(self):
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


def coroutine_(fn):
    co = coroutine(fn)
    parameters = signature(fn).parameters
    num_outputs = len(parameters)
    outputs = [Output() for _ in range(num_outputs)]
    class wrapper:
        def __init__(self):
            self.co = co(*outputs)
            self.outputs = outputs
            for name, output in zip(parameters, outputs):
                setattr(self, name, output)

        def send(self, *args, **kwargs):
            self.co.send(*args, **kwargs)
    return wrapper


def wire(a, b):
    a.outputs.append(b)

def DefineReg(width, init=0):
    @coroutine_
    def _Reg(output):
        x = init
        while True:
            x_next = yield
            output.send(x)
            x = x_next
    return _Reg


@coroutine
def test_vector_checker(expected):
    while True:
        for e in expected:
            x = yield
            assert x == e


@coroutine
def printer():
    while True:
        for e in expected:
            x = yield
            print(x, end=" ")


if __name__ == "__main__":
    inputs = [1, 0, 0, 1, 1, 0, 1, 1, 0]
    expected = [0] + inputs[:-1]
    reg4 = DefineReg(4)()
    checker = test_vector_checker(expected)
    printer = printer()
    wire(reg4.output, checker)
    wire(reg4.output, printer)
    print("Expected : {}".format(" ".join(str(x) for x in expected)))
    print("Actual   : ", end="")
    for i in inputs:
        reg4.send(i)
