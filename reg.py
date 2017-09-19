from coroutine import coroutine

@coroutine
def Reg(init=0):
    value = init
    while True:
        value = yield
