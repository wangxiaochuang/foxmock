from foxmock import Mock
import pytest

def test_base():
    mock = Mock()
    mock.call("foo").ret("bar")
    mock.index("name").ret("jack")

    assert mock["name"] == "jack"
    assert mock.name == "jack"
    assert mock.foo() == "bar"