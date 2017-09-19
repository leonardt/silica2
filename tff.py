from coroutine import coroutine
from reg import Reg

@coroutine
def TFF():
    reg = Reg()
    O = reg.value
    while True:
        I = yield
        O = reg.value
        reg.send(I ^ O)

tff = TFF()
for bit in [0, 1, 0, 0, 1, 1]:
    tff.send(bit)
    print(tff.O, end=" ")
