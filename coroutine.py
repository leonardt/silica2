import types


def coroutine(func):
    class Coroutine:
        def __init__(self, *args, **kwargs):
            self.definition = func
            self.internal_values = {}
            self.reset(*args, **kwargs)

        def reset(self, *args, **kwargs):
            self.co = types.coroutine(self.definition)(*args, **kwargs)
            next(self.co)

        def __getattr__(self, key):
            return self.co.gi_frame.f_locals[key]

        def send(self, *args, **kwargs):
            return self.co.send(*args, **kwargs)

        def __next__(self):
            return next(self.co)
    return Coroutine
