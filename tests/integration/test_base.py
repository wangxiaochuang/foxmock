from foxmock import Mock
import pytest

def test_base():
    mock = Mock()
    mock.call("foo").ret("bar")
    mock.index("name").ret("jack")
    mock.index("name1").ret("jack1")

    assert mock["name"] == "jack"
    assert mock["name1"] == "jack1"
    assert mock.name == "jack"
    assert mock.name1 == "jack1"
    assert mock.foo() == "bar"
    assert mock.get_history(0).func == "foo"

def test_except():
    mock = Mock()
    try:
        assert mock["name"] == "xxxxx"
    except RuntimeError:
        pass

    try:
        assert mock.run() == "xxxxx"
    except RuntimeError:
        pass

    mock.call("foo").ret("bar")
    assert mock.foo() == "bar"
    try:
        assert mock.foo("xxx") == "xxxxx"
    except RuntimeError:
        pass


def test_mock_with_args():
    mock = Mock()
    mock.call("foo").with_args(123).ret("123bar")
    mock.call("foo").with_args("123").ret("'123'bar")

    assert mock.foo(123) == "123bar"
    assert mock.foo('123') == "'123'bar"

class MyClass():
    def __init__(self):
        self.a = 'a'
        self.b = 'b'

def test_mock_with_object():
    mock = Mock()
    mock.call("foo").with_args(MyClass()).ret(123)
    mock.foo(MyClass())