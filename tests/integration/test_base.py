from foxmock import Mock
import pytest

def test_base():
    mock = Mock()
    mock.call("foo").ret("bar")
    mock.index("name").ret("jack")

    assert mock["name"] == "jack"
    assert mock.name == "jack"
    assert mock.foo() == "bar"

def test_mock_with_args():
    mock = Mock()
    mock.call("foo").with_args(123).ret("123bar")
    mock.call("foo").with_args("123").ret("'123'bar")

    assert mock.foo(123) == "123bar"
    assert mock.foo('123') == "'123'bar"