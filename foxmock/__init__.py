from __future__ import annotations
import json

class Encoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class Key():
    def __init__(self, args, kwargs):
        self.args = json.dumps(args, cls=Encoder)
        self.kwargs = json.dumps(kwargs, cls=Encoder)
    
    def __key(self):
        return (self.args, self.kwargs)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.__key() == other.__key()
        return NotImplemented
        

class Resp():
    def __init__(self):
        self.resp = None
    def ret(self, resp):
        self.resp = resp
    def get_resp(self):
        return self.resp

class Method():
    def __init__(self, name: str) -> None:
        self.name = name
        self.reqs = {}

    def ret(self, val):
        resp = Resp()
        self.reqs[Key((), {})] = resp
        resp.ret(val)
    
    def get_resp_or_create(self, key) -> Resp:
        resp = self.reqs.get(key)
        if resp:
            return resp
        self.reqs[key] = Resp()
        return self.reqs[key]
        
    def with_args(self, *args, **kwargs) -> Resp:
        return self.get_resp_or_create(Key(args, kwargs))

class CallArg():
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __repr__(self) -> str:
        return f"{self.func}({self.args}, {self.kwargs})"

class Runner(Method):
    def __init__(self, name: str, history: list):
        super().__init__(name)
        self.history = history
        self.name = name

    def __call__(self, *args, **kwargs):
        self.history.append(CallArg(self.name, args, kwargs))
        if resp := self.reqs.get(Key(args, kwargs)):
            return resp.get_resp()
        raise RuntimeError(f"not mock for method: {self.name}({args}, {kwargs})")

class Mock():
    def __init__(self):
        self.__runners = {}
        self.__indexers = {}
        self.__history = []
    
    def get_histories(self):
        return self.__history

    def get_history(self, idx):
        return self.__history[idx]

    def __get_or_create_runner(self, name):
        runner = self.__runners.get(name)
        if not runner:
            runner = Runner(name, self.__history)
            self.__runners[name] = runner
        return runner
        
    def call(self, name: str):
        runner = self.__get_or_create_runner(name)
        setattr(self, name, runner)
        return runner

    def __get_or_create_indexer(self, name):
        indexer = self.__indexers.get(name)
        if not indexer:
            indexer = Resp()
            self.__indexers[name] = indexer
        return indexer

    def index(self, name):
        indexer = self.__get_or_create_indexer(name)
        return indexer

    def __getitem__(self, name):
        if indexer := self.__indexers.get(name):
            return indexer.get_resp()
        raise RuntimeError(f"not mock for index: {name}")
    
    __getattr__ = __getitem__
