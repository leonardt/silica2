from coroutine import coroutine
from magma.bitutils import int2seq


def uart_transmit(data):
    yield 0
    yield from data
    # for d in data:
    #     yield d
    yield 1


def uart_receive():
    data = [0 for _ in range(8)]
    while True:
        RX = yield
        if RX == 0:
            for i in range(8):
                data[i] = yield
            RX = yield
            if RX == 1:
                return data

@coroutine
def main():
    while True:
        value = yield from uart_receive()
        yield from uart_transmit(value)

main_ = main()

data = int2seq(0xBE)
print("Expected: 0 " + " ".join(str(x) for x in data) + " 1")
print("Actual  : ", end="")
for RX in [0] + data + [1]:
    transmit_bit = main_.send(RX)
print(transmit_bit, end=" ")  # First bit is sent on last bit

for _ in range(len(data) + 1):
    transmit_bit = main_.send(None)
    print(transmit_bit, end=" ")
