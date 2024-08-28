from foxmock import Mock
import pytest

def test_base():
    mock = Mock()
    mock.call("foo").ret("bar")

    # assert mock["name"] == "jack"