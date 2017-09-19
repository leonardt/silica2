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
