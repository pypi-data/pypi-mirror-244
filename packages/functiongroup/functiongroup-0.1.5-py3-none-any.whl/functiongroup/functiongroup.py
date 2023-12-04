import functools


class FunctionGroup:
    def __init__(self):
        self.functions = []

    def register(self, func):
        self.functions.append(func)

    def __call__(self, *args, **kwargs):
        class FunctionGroupInstance:
            pass

        instance = FunctionGroupInstance()
        for func in self.functions:
            setattr(instance, func.__name__,
                    functools.partial(func, *args, **kwargs))
        return instance
