import pytest


def test_lacking_copy_ctor():
    from pybind11_tests import lacking_copy_ctor
    with pytest.raises(RuntimeError) as excinfo:
        lacking_copy_ctor.get_one()
    if "the object is non-copyable!" not in str(excinfo.value):
        raise AssertionError


def test_lacking_move_ctor():
    from pybind11_tests import lacking_move_ctor
    with pytest.raises(RuntimeError) as excinfo:
        lacking_move_ctor.get_one()
    if "the object is neither movable nor copyable!" not in str(excinfo.value):
        raise AssertionError
