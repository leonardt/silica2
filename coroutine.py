# Adapted for Python 3 from http://www.dabeaz.com/coroutines/coroutine.py
# coroutine.py
#
# A decorator function that takes care of starting a coroutine
# automatically on call.
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


def coroutine(func):
    def start(*args,**kwargs):
        # cr = func(*args,**kwargs)
        # next(cr)
        cr = types.coroutine(func)(*args,**kwargs)
        return Coroutine(cr)
    return start

# Example use
if __name__ == '__main__':
    @coroutine
    def grep(pattern):
        print("Looking for %s" % pattern)
        while True:
            line = (yield)
            if pattern in line:
                print(line)

    g = grep("python")
    # Notice how you don't need a next() call here
    g.send("Yeah, but no, but yeah, but no")
    g.send("A series of tubes")
    g.send("python generators rock!")
