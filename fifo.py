from coroutine import coroutine
from magma.bitutils import int2seq, seq2int
import numpy as np


class Fifo:
    def __init__(self, height=2, width=None):
        self.height = height
        self.width = width
        if width is None:
            self._values = np.ndarray(height, np.bool)
        else:
            self._values = np.ndarray((height, width), np.bool)
        self._curr_write_idx = 1
        self._curr_read_idx = 0

    def push(self, value):
        if self._curr_write_idx == self._curr_read_idx:
            return
        self._values[self._curr_write_idx] = value
        self._curr_write_idx += 1
        if self._curr_write_idx == self.height:
            self._curr_write_idx = 0

    def pop(self):
        if self._curr_read_idx == self._curr_write_idx - 1:
            return None
        self._curr_read_idx += 1
        if self._curr_read_idx == self.height:
            self._curr_read_idx = 0
        value = self._values[self._curr_read_idx]
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
