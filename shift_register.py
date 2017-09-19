from coroutine import coroutine
from reg import Reg


@coroutine
def ShiftRegister(length):
    regs = [Reg() for _ in range(length)]
    curr = None
    while True:
        I = yield curr
        curr = I
        for reg in regs:
            curr, _ = reg.value, reg.send(curr)


shift_register = ShiftRegister(3)
sequence = [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1]
print("Inputs ", " ".join(str(x) for x in sequence))
print("Outputs ", end="")
for bit in sequence:
    print(shift_register.send(bit), end=" ")
