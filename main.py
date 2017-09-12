from coroutine import coroutine


def DefineReg(width, init=0):
    @coroutine
    def _Reg(output):
        x = init
        while True:
            output.send(x)
            x = yield
    return _Reg


@coroutine
def test_vector_checker(expected):
    while True:
        for e in expected:
            x = yield
            print("Got {}, expected {}".format(x, e))
            assert x == e


if __name__ == "__main__":
    inputs = [1, 0, 0, 1, 1, 0, 1, 1, 0]
    expected = [0] + inputs
    reg = DefineReg(4)(test_vector_checker(expected))
    for i in inputs:
        reg.send(i)
