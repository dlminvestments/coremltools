

def test_constants():
    from pybind11_tests import some_constant

    if some_constant != 14:
        raise AssertionError


def test_function_overloading():
    from pybind11_tests import MyEnum, test_function

    if test_function() != "test_function()":
        raise AssertionError
    if test_function(7) != "test_function(7)":
        raise AssertionError
    if test_function(MyEnum.EFirstEntry) != "test_function(enum=1)":
        raise AssertionError
    if test_function(MyEnum.ESecondEntry) != "test_function(enum=2)":
        raise AssertionError

    if test_function(1, 1.0) != "test_function(int, float)":
        raise AssertionError
    if test_function(2.0, 2) != "test_function(float, int)":
        raise AssertionError


def test_bytes():
    from pybind11_tests import return_bytes, print_bytes

    if print_bytes(return_bytes()) != "bytes[1 0 2 0]":
        raise AssertionError


def test_exception_specifiers():
    from pybind11_tests.exc_sp import C, f1, f2, f3, f4

    c = C()
    if c.m1(2) != 1:
        raise AssertionError
    if c.m2(3) != 1:
        raise AssertionError
    if c.m3(5) != 2:
        raise AssertionError
    if c.m4(7) != 3:
        raise AssertionError
    if c.m5(10) != 5:
        raise AssertionError
    if c.m6(14) != 8:
        raise AssertionError
    if c.m7(20) != 13:
        raise AssertionError
    if c.m8(29) != 21:
        raise AssertionError

    if f1(33) != 34:
        raise AssertionError
    if f2(53) != 55:
        raise AssertionError
    if f3(86) != 89:
        raise AssertionError
    if f4(140) != 144:
        raise AssertionError
