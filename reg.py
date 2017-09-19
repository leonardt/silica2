from coroutine import coroutine

init = 0

@coroutine
def Reg():
    curr_value = next_value = 0
    while True:
        tmp = yield curr_value
        curr_value, next_value = next_value, tmp

reg = Reg()
print("Input 1, Output {}".format(reg.send(1)))
print("Input 0, Output {}".format(reg.send(0)))
print("Input 0, Output {}".format(reg.send(0)))
print("Input 1, Output {}".format(reg.send(1)))
print("Input 1, Output {}".format(reg.send(1)))
print("Input 1, Output {}".format(reg.send(1)))
