try:
    from interface.pyxxusb import _pyxxusb as pycc # Here it is used only for comunicationg with the CC-USB
except Exception as e:
    print(e)
    print("pyxxusb lib works only with python 32bit")
    print("The PC should be connected to the cc-usb")


def gen_command(N, A, F):
    return F + 32*A + 512*N

def stack_as_longArray(stack):
    stack_ar = pycc.new_longArray(len(stack))
    for i,e in enumerate(stack):
        pycc.longArray_setitem(stack_ar, i, e)
    return stack_ar

def generate_stack(*commands:list, marker=True):
    nofc = len(commands) + 2*marker
    res = [nofc]
    for l in commands:
        N, A, F = l
        res.append(gen_command(N, A, F))
    if marker:
        res.append(gen_command(0, 0, 16))
        res.append(int("0xFFFF", 16))
    return stack_as_longArray(res)