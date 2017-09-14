from coroutine import coroutine
from magma.bitutils import int2seq, seq2int
from magma.bit_vector import BitVector
import numpy as np


class Fifo:
    def __init__(self, depth=2, width=None):
        if width is None:
            self._values = np.ndarray(depth, np.bool)
        else:
            self._values = np.ndarray((depth, width), np.bool)
        addr_width = (depth - 1).bit_length()
        self._curr_write_idx = BitVector(1, num_bits=addr_width)
        self._curr_read_idx = BitVector(0, num_bits=addr_width)

    def push(self, value):
        if self._curr_write_idx == self._curr_read_idx:
            return
        self._values[self._curr_write_idx.as_int()] = value
        self._curr_write_idx += BitVector(1, num_bits=len(self._curr_write_idx))

    def pop(self):
        if self._curr_read_idx == \
                self._curr_write_idx - BitVector(1, num_bits=len(self._curr_read_idx)):
            return None
        self._curr_read_idx += BitVector(1, num_bits=len(self._curr_read_idx))
        value = self._values[self._curr_read_idx.as_int()]
        return value


@coroutine
def main():
    fifo = Fifo(2, 3)
    while True:
        x = yield fifo.pop()
        fifo.push(x)
        x = yield
        fifo.push(x)

co = main()
for i in range(8):
    result = co.send(int2seq(i, 3))
    if result is not None:
        result = seq2int(result)
    print("Got  : {}".format(result))
