
def test_nested_modules():
    import pybind11_tests
    from pybind11_tests.submodule import submodule_func

    if pybind11_tests.__name__ != "pybind11_tests":
        raise AssertionError
    if pybind11_tests.submodule.__name__ != "pybind11_tests.submodule":
        raise AssertionError

    if submodule_func() != "submodule_func()":
        raise AssertionError


def test_reference_internal():
    from pybind11_tests import ConstructorStats
    from pybind11_tests.submodule import A, B

    b = B()
    if str(b.get_a1()) != "A[1]":
        raise AssertionError
    if str(b.a1) != "A[1]":
        raise AssertionError
    if str(b.get_a2()) != "A[2]":
        raise AssertionError
    if str(b.a2) != "A[2]":
        raise AssertionError

    b.a1 = A(42)
    b.a2 = A(43)
    if str(b.get_a1()) != "A[42]":
        raise AssertionError
    if str(b.a1) != "A[42]":
        raise AssertionError
    if str(b.get_a2()) != "A[43]":
        raise AssertionError
    if str(b.a2) != "A[43]":
        raise AssertionError

    astats, bstats = ConstructorStats.get(A), ConstructorStats.get(B)
    if astats.alive() != 2:
        raise AssertionError
    if bstats.alive() != 1:
        raise AssertionError
    del b
    if astats.alive() != 0:
        raise AssertionError
    if bstats.alive() != 0:
        raise AssertionError
    if astats.values() != ['1', '2', '42', '43']:
        raise AssertionError
    if bstats.values() != []:
        raise AssertionError
    if astats.default_constructions != 0:
        raise AssertionError
    if bstats.default_constructions != 1:
        raise AssertionError
    if astats.copy_constructions != 0:
        raise AssertionError
    if bstats.copy_constructions != 0:
        raise AssertionError
    # assert astats.move_constructions >= 0  # Don't invoke any
    # assert bstats.move_constructions >= 0  # Don't invoke any
    if astats.copy_assignments != 2:
        raise AssertionError
    if bstats.copy_assignments != 0:
        raise AssertionError
    if astats.move_assignments != 0:
        raise AssertionError
    if bstats.move_assignments != 0:
        raise AssertionError


def test_importing():
    from pybind11_tests import OD
    from collections import OrderedDict

    if OD is not OrderedDict:
        raise AssertionError
    if str(OD([(1, 'a'), (2, 'b')])) != "OrderedDict([(1, 'a'), (2, 'b')])":
        raise AssertionError
