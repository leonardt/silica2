from coroutine import coroutine
from magma.bit_vector import BitVector
from magma.bitutils import int2seq, seq2int
import numpy as np


class Fifo:
    def __init__(self, depth=2, width=None):
        if width is None:
            self._values = np.ndarray(depth, np.int)
        else:
            self._values = np.ndarray((depth, width), np.int)
        # We use an extra bit to optimize the full/empty comparison
        addr_width = (depth - 1).bit_length() + 1
        self._curr_write_idx = BitVector(0, num_bits=addr_width)
        self._curr_read_idx = BitVector(0, num_bits=addr_width)

    def push(self, value):
        if self._curr_read_idx[1:] == self._curr_write_idx[1:] and \
                self._curr_read_idx[0] != self._curr_write_idx[0]:
            # print("Fifo stalled because full")
            yield
        self._values[self._curr_write_idx[1:].as_int()] = value
        self._curr_write_idx += BitVector(1, num_bits=len(self._curr_write_idx))

    def pop(self):
        if self._curr_read_idx[1:] == self._curr_write_idx[1:] and \
                self._curr_read_idx[0] == self._curr_write_idx[0]:
            yield
        self._curr_read_idx += BitVector(1, num_bits=len(self._curr_read_idx))
        value = self._values[self._curr_read_idx[1:].as_int()]
        return value


@coroutine
def uart_transmit(fifo):
    while True:
        data = yield from fifo.pop()
        yield 0
        yield from data
        yield 1


@coroutine
def uart_receive(fifo):
    data = [0 for _ in range(8)]
    while True:
        RX = yield
        if RX == 0:
            for i in range(8):
                data[i] = yield
            RX = yield
            if RX == 1:
                print("uart_receive got : {} ({:X})".format(data, seq2int(data)))
                yield from fifo.push(data)

fifo = Fifo(depth=2, width=8)
receive = uart_receive(fifo)
transmit = uart_transmit(fifo)

for data in [0xDE, 0xAD, 0xBE, 0xEF]:
    data = int2seq(data)
    print("Sending: 0 " + " ".join(str(x) for x in data) + " 1")
    for RX in [0] + data + [1]:
        receive.send(RX)

for i in range(3):
    tx = []
    for _ in range(len(data) + 2):
        tx.append(next(transmit))
    print("Transmitted: {} ({:X})".format(tx[1:-1], seq2int(tx[1:-1])))
