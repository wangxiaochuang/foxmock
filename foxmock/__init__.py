from typing import Any


class Method():
    def __init__(self, name: str) -> None:
        self.name = name
        self.return_value = None

    def ret(self, val):
        self.return_value = val

class CallArg():
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

class Runner(Method):
    def __init__(self, name: str):
        super().__init__(name)
        self.history = []
    def __call__(self, *args, **kwargs):
        self.history.append(CallArg(args, kwargs))
        return self.return_value

class Index(Method):
    def __getitem__(self, name):
        if name != self.name:
            raise KeyError(name)
        return self.return_value
    
    __getattr__ = __getitem__
    

class Mock():
    def call(self, name: str):
        runner = Runner(name)
        setattr(self, name, runner)
        return runner

    def index(self, name):
        indexer = Index(name)
        setattr(self, "_indexer", indexer)
        return indexer


    def __getitem__(self, name):
        return self._indexer[name]
    
    __getattr__ = __getitem__
