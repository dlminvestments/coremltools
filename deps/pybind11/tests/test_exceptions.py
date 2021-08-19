import pytest


def test_error_already_set(msg):
    from pybind11_tests import throw_already_set

    with pytest.raises(RuntimeError) as excinfo:
        throw_already_set(False)
    if msg(excinfo.value) != "Unknown internal error occurred":
        raise AssertionError

    with pytest.raises(ValueError) as excinfo:
        throw_already_set(True)
    if msg(excinfo.value) != "foo":
        raise AssertionError


def test_python_call_in_catch():
    from pybind11_tests import python_call_in_destructor

    d = {}
    if python_call_in_destructor(d) is not True:
        raise AssertionError
    if d["good"] is not True:
        raise AssertionError


def test_custom(msg):
    from pybind11_tests import (MyException, MyException5, MyException5_1,
                                throws1, throws2, throws3, throws4, throws5, throws5_1,
                                throws_logic_error)

    # Can we catch a MyException?"
    with pytest.raises(MyException) as excinfo:
        throws1()
    if msg(excinfo.value) != "this error should go to a custom type":
        raise AssertionError

    # Can we translate to standard Python exceptions?
    with pytest.raises(RuntimeError) as excinfo:
        throws2()
    if msg(excinfo.value) != "this error should go to a standard Python exception":
        raise AssertionError

    # Can we handle unknown exceptions?
    with pytest.raises(RuntimeError) as excinfo:
        throws3()
    if msg(excinfo.value) != "Caught an unknown exception!":
        raise AssertionError

    # Can we delegate to another handler by rethrowing?
    with pytest.raises(MyException) as excinfo:
        throws4()
    if msg(excinfo.value) != "this error is rethrown":
        raise AssertionError

    # "Can we fall-through to the default handler?"
    with pytest.raises(RuntimeError) as excinfo:
        throws_logic_error()
    if msg(excinfo.value) != "this error should fall through to the standard handler":
        raise AssertionError

    # Can we handle a helper-declared exception?
    with pytest.raises(MyException5) as excinfo:
        throws5()
    if msg(excinfo.value) != "this is a helper-defined translated exception":
        raise AssertionError

    # Exception subclassing:
    with pytest.raises(MyException5) as excinfo:
        throws5_1()
    if msg(excinfo.value) != "MyException5 subclass":
        raise AssertionError
    if not isinstance(excinfo.value, MyException5_1):
        raise AssertionError

    with pytest.raises(MyException5_1) as excinfo:
        throws5_1()
    if msg(excinfo.value) != "MyException5 subclass":
        raise AssertionError

    with pytest.raises(MyException5) as excinfo:
        try:
            throws5()
        except MyException5_1:
            raise RuntimeError("Exception error: caught child from parent")
    if msg(excinfo.value) != "this is a helper-defined translated exception":
        raise AssertionError
