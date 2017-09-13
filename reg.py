from coroutine import coroutine

init = 0

@coroutine
def Reg():
    value1 = value2 = 0
    while True:
        value1 = yield value1
        value2 = yield value2

reg = Reg()
print(reg.send(1))
print(reg.send(2))
print(reg.send(3))
