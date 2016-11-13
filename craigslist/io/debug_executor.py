class DebugExecutor:
    def __init__(self, max_workers=None):
        pass

    def submit(self, fn, *args, **kwargs):
        return DebugFuture(fn, *args, **kwargs)

class DebugFuture:
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self._condition = DebugCondition()
        self._state = 'FINISHED'
        self._waiters = []

    def result(self):
        return self.fn(*self.args, **self.kwargs)

class DebugCondition:
    def __init__(self):
        self.acquire = lambda: None
        self.release = lambda: None

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

