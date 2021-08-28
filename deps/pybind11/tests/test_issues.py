import pytest
from pybind11_tests import ConstructorStats


def test_regressions():
    from pybind11_tests.issues import print_cchar, print_char

    # #137: const char* isn't handled properly
    if print_cchar("const char *") != "const char *":
        raise AssertionError
    # #150: char bindings broken
    if print_char("c") != "c":
        raise AssertionError


def test_dispatch_issue(msg):
    """#159: virtual function dispatch has problems with similar-named functions"""
    from pybind11_tests.issues import DispatchIssue, dispatch_issue_go

    class PyClass1(DispatchIssue):
        @staticmethod
        def dispatch():
            return "Yay.."

    class PyClass2(DispatchIssue):
        def dispatch(self):
            with pytest.raises(RuntimeError) as excinfo:
                super(PyClass2, self).dispatch()
            if msg(excinfo.value) != 'Tried to call pure virtual function "Base::dispatch"':
                raise AssertionError

            p = PyClass1()
            return dispatch_issue_go(p)

    b = PyClass2()
    if dispatch_issue_go(b) != "Yay..":
        raise AssertionError


def test_reference_wrapper():
    """#171: Can't return reference wrappers (or STL data structures containing them)"""
    from pybind11_tests.issues import Placeholder, return_vec_of_reference_wrapper

    if str(return_vec_of_reference_wrapper(Placeholder(4))) != "[Placeholder[1], Placeholder[2], Placeholder[3], Placeholder[4]]":
        raise AssertionError


def test_iterator_passthrough():
    """#181: iterator passthrough did not compile"""
    from pybind11_tests.issues import iterator_passthrough

    if list(iterator_passthrough(iter([3, 5, 7, 9, 11, 13, 15]))) != [3, 5, 7, 9, 11, 13, 15]:
        raise AssertionError


def test_shared_ptr_gc():
    """// #187: issue involving std::shared_ptr<> return value policy & garbage collection"""
    from pybind11_tests.issues import ElementList, ElementA

    el = ElementList()
    for i in range(10):
        el.add(ElementA(i))
    pytest.gc_collect()
    for i, v in enumerate(el.get()):
        if i != v.value():
            raise AssertionError


def test_no_id(msg):
    from pybind11_tests.issues import get_element, expect_float, expect_int

    with pytest.raises(TypeError) as excinfo:
        get_element(None)
    if msg(excinfo.value) != """
        get_element(): incompatible function arguments. The following argument types are supported:
            1. (arg0: m.issues.ElementA) -> int

        Invoked with: None
    """:
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        expect_int(5.2)
    if msg(excinfo.value) != """
        expect_int(): incompatible function arguments. The following argument types are supported:
            1. (arg0: int) -> int

        Invoked with: 5.2
    """:
        raise AssertionError
    if expect_float(12) != 12:
        raise AssertionError


def test_str_issue(msg):
    """Issue #283: __str__ called on uninitialized instance when constructor arguments invalid"""
    from pybind11_tests.issues import StrIssue

    if str(StrIssue(3)) != "StrIssue[3]":
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        str(StrIssue("no", "such", "constructor"))
    if msg(excinfo.value) != """
        __init__(): incompatible constructor arguments. The following argument types are supported:
            1. m.issues.StrIssue(arg0: int)
            2. m.issues.StrIssue()

        Invoked with: 'no', 'such', 'constructor'
    """:
        raise AssertionError


def test_nested():
    """ #328: first member in a class can't be used in operators"""
    from pybind11_tests.issues import NestA, NestB, NestC, get_NestA, get_NestB, get_NestC

    a = NestA()
    b = NestB()
    c = NestC()

    a += 10
    if get_NestA(a) != 13:
        raise AssertionError
    b.a += 100
    if get_NestA(b.a) != 103:
        raise AssertionError
    c.b.a += 1000
    if get_NestA(c.b.a) != 1003:
        raise AssertionError
    b -= 1
    if get_NestB(b) != 3:
        raise AssertionError
    c.b -= 3
    if get_NestB(c.b) != 1:
        raise AssertionError
    c *= 7
    if get_NestC(c) != 35:
        raise AssertionError

    abase = a.as_base()
    if abase.value != -2:
        raise AssertionError
    a.as_base().value += 44
    if abase.value != 42:
        raise AssertionError
    if c.b.a.as_base().value != -2:
        raise AssertionError
    c.b.a.as_base().value += 44
    if c.b.a.as_base().value != 42:
        raise AssertionError

    del c
    pytest.gc_collect()
    del a  # Should't delete while abase is still alive
    pytest.gc_collect()

    if abase.value != 42:
        raise AssertionError
    del abase, b
    pytest.gc_collect()


def test_move_fallback():
    from pybind11_tests.issues import get_moveissue1, get_moveissue2
    m2 = get_moveissue2(2)
    if m2.value != 2:
        raise AssertionError
    m1 = get_moveissue1(1)
    if m1.value != 1:
        raise AssertionError


def test_override_ref():
    from pybind11_tests.issues import OverrideTest
    o = OverrideTest("asdf")

    # Not allowed (see associated .cpp comment)
    # i = o.str_ref()
    # assert o.str_ref() == "asdf"
    if o.str_value() != "asdf":
        raise AssertionError

    if o.A_value().value != "hi":
        raise AssertionError
    a = o.A_ref()
    if a.value != "hi":
        raise AssertionError
    a.value = "bye"
    if a.value != "bye":
        raise AssertionError


def test_operators_notimplemented(capture):
    from pybind11_tests.issues import OpTest1, OpTest2
    with capture:
        c1, c2 = OpTest1(), OpTest2()
        c1 + c1
        c2 + c2
        c2 + c1
        c1 + c2
    if capture != """
        Add OpTest1 with OpTest1
        Add OpTest2 with OpTest2
        Add OpTest2 with OpTest1
        Add OpTest2 with OpTest1
    """:
        raise AssertionError


def test_iterator_rvpolicy():
    """ Issue 388: Can't make iterators via make_iterator() with different r/v policies """
    from pybind11_tests.issues import make_iterator_1
    from pybind11_tests.issues import make_iterator_2

    if list(make_iterator_1()) != [1, 2, 3]:
        raise AssertionError
    if list(make_iterator_2()) != [1, 2, 3]:
        raise AssertionError
    if isinstance(make_iterator_1(), type(make_iterator_2())):
        raise AssertionError


def test_dupe_assignment():
    """ Issue 461: overwriting a class with a function """
    from pybind11_tests.issues import dupe_exception_failures
    if dupe_exception_failures() != []:
        raise AssertionError


def test_enable_shared_from_this_with_reference_rvp():
    """ Issue #471: shared pointer instance not dellocated """
    from pybind11_tests import SharedParent, SharedChild

    parent = SharedParent()
    child = parent.get_child()

    cstats = ConstructorStats.get(SharedChild)
    if cstats.alive() != 1:
        raise AssertionError
    del child, parent
    if cstats.alive() != 0:
        raise AssertionError


def test_non_destructed_holders():
    """ Issue #478: unique ptrs constructed and freed without destruction """
    from pybind11_tests import SpecialHolderObj

    a = SpecialHolderObj(123)
    b = a.child()

    if a.val != 123:
        raise AssertionError
    if b.val != 124:
        raise AssertionError

    cstats = SpecialHolderObj.holder_cstats()
    if cstats.alive() != 1:
        raise AssertionError
    del b
    if cstats.alive() != 1:
        raise AssertionError
    del a
    if cstats.alive() != 0:
        raise AssertionError


def test_complex_cast(capture):
    """ Issue #484: number conversion generates unhandled exceptions """
    from pybind11_tests.issues import test_complex

    with capture:
        test_complex(1)
        test_complex(2j)

    if capture != """
        1.0
        (0.0, 2.0)
    """:
        raise AssertionError


def test_inheritance_override_def_static():
    from pybind11_tests.issues import MyBase, MyDerived

    b = MyBase.make()
    d1 = MyDerived.make2()
    d2 = MyDerived.make()

    if not isinstance(b, MyBase):
        raise AssertionError
    if not isinstance(d1, MyDerived):
        raise AssertionError
    if not isinstance(d2, MyDerived):
        raise AssertionError
