# foxmock

a mock library for python, It's simple and flixible

```python
from foxmock import Mock

obj = Mock()
obj.call("get").ret("12345")
obj.index("age").ret(32)

token = obj.get()
assert token == "12345"
assert obj["age"] == 32
```

or you can inherit from Mock

```python
from foxmock import Mock

class DynamicToken(Mock):
    def __init__(self):
        self.call("get").ret("12345")
        self.index("age").ret(32)


token = obj.get()
assert token == "12345"
assert obj["age"] == 32
```
