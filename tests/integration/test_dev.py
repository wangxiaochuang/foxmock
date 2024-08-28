from foxmock import Mock
import pytest

def test_mock_with_args():
    mock = Mock()
    mock.call("foo").with_args(123).ret("123bar")
    mock.call("foo").with_args("123").ret("'123'bar")

    assert mock.foo(123) == "123bar"
    assert mock.foo('123') == "'123'bar"