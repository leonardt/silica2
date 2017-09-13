from coroutine import coroutine
from magma.bitutils import int2seq


def tx(data):
    yield 0
    yield from data
    # for d in data:
    #     yield d
    yield 1


@coroutine
def uart_rx():
    data = [0 for _ in range(8)]
    while True:
        RX = yield
        if RX == 0:
            for i in range(8):
                data[i] = yield
            RX = yield
            if RX == 1:
                yield data


@coroutine
def main():
    rx = uart_rx()
    while True:
        value = None
        while value is None:
            RX = yield
            value = rx.send(RX)
        yield from tx(value)

main_ = main()

data = int2seq(0xBE)
print("Expected: 0 " + " ".join(str(x) for x in data) + " 1")
print("Actual  : ", end="")
for RX in [0] + data + [1]:
    TX = main_.send(RX)
print(TX, end=" ")  # First bit is sent on last bit

for _ in range(len(data) + 1):
    TX = main_.send(None)
    print(TX, end=" ")
