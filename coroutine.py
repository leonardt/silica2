import types

class Coroutine():
    def __init__(self, co):
        self.co = co
        self.running = False

    def send(self, *args, **kwargs):
        if self.running is False:
            next(self.co)
            self.running = True
        return self.co.send(*args, **kwargs)

    def __next__(self):
        self.running = True
        return next(self.co)


def coroutine(func):
    def start(*args,**kwargs):
        cr = types.coroutine(func)(*args,**kwargs)
        return Coroutine(cr)
    return start
