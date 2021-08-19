import pytest


def test_string_list():
    from pybind11_tests import StringList, ClassWithSTLVecProperty, print_opaque_list

    l = StringList()
    l.push_back("Element 1")
    l.push_back("Element 2")
    if print_opaque_list(l) != "Opaque list: [Element 1, Element 2]":
        raise AssertionError
    if l.back() != "Element 2":
        raise AssertionError

    for i, k in enumerate(l, start=1):
        if k != "Element {}".format(i):
            raise AssertionError
    l.pop_back()
    if print_opaque_list(l) != "Opaque list: [Element 1]":
        raise AssertionError

    cvp = ClassWithSTLVecProperty()
    if print_opaque_list(cvp.stringList) != "Opaque list: []":
        raise AssertionError

    cvp.stringList = l
    cvp.stringList.push_back("Element 3")
    if print_opaque_list(cvp.stringList) != "Opaque list: [Element 1, Element 3]":
        raise AssertionError


def test_pointers(msg):
    from pybind11_tests import (return_void_ptr, get_void_ptr_value, ExampleMandA,
                                print_opaque_list, return_null_str, get_null_str_value,
                                return_unique_ptr, ConstructorStats)

    living_before = ConstructorStats.get(ExampleMandA).alive()
    if get_void_ptr_value(return_void_ptr()) != 0x1234:
        raise AssertionError
    if not get_void_ptr_value(ExampleMandA()):
        raise AssertionError
    if ConstructorStats.get(ExampleMandA).alive() != living_before:
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        get_void_ptr_value([1, 2, 3])  # This should not work
    if msg(excinfo.value) != """
        get_void_ptr_value(): incompatible function arguments. The following argument types are supported:
            1. (arg0: capsule) -> int

        Invoked with: [1, 2, 3]
    """:
        raise AssertionError

    if return_null_str() is not None:
        raise AssertionError
    if get_null_str_value(return_null_str()) is None:
        raise AssertionError

    ptr = return_unique_ptr()
    if "StringList" not in repr(ptr):
        raise AssertionError
    if print_opaque_list(ptr) != "Opaque list: [some value]":
        raise AssertionError
