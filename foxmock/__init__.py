class Method():
    def __init__(self, name) -> None:
        self.name = name
        self.return_value = None

    def ret(self, val):
        self.return_value = val

class Runner(Method):
    def __call__(self, *args, **kwargs):
        return self.return_value

class Index(Method):
    def __getitem__(self, name):
        if name != self.name:
            raise KeyError(name)
        return self.return_value
    

class Mock():
    def call(self, name):
        runner = Runner(name)
        setattr(self, name, runner)
        return runner

    def index(self, name):
        indexer = Index(name)
        setattr(self, "_indexer", indexer)
        return indexer


    def __getitem__(self, name):
        return self._indexer[name]
