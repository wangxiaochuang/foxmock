from __future__ import annotations
import json

class Key():
    def __init__(self, args, kwargs):
        self.args = json.dumps(args)
        self.kwargs = json.dumps(kwargs)
    
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
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

class Runner(Method):
    def __init__(self, name: str):
        super().__init__(name)
        self.history = []
    def __call__(self, *args, **kwargs):
        self.history.append(CallArg(args, kwargs))
        if resp := self.reqs.get(Key(args, kwargs)):
            return resp.get_resp()
        raise RuntimeError("No response for call")

class Mock():
    def __init__(self):
        self.__runners = {}
        self.__indexers = {}
    
    def __get_or_create_runner(self, name):
        runner = self.__runners.get(name)
        if not runner:
            runner = Runner(name)
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
        raise RuntimeError("No response for call")
    
    __getattr__ = __getitem__
