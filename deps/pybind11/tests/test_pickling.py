import pytest

try:
    import cPickle as pickle  # Use cPickle on Python 2.7
except ImportError:
    import pickle


def test_roundtrip():
    from pybind11_tests import Pickleable

    p = Pickleable("test_value")
    p.setExtra1(15)
    p.setExtra2(48)

    data = pickle.dumps(p, 2)  # Must use pickle protocol >= 2
    p2 = pickle.loads(data)
    if p2.value() != p.value():
        raise AssertionError
    if p2.extra1() != p.extra1():
        raise AssertionError
    if p2.extra2() != p.extra2():
        raise AssertionError


@pytest.unsupported_on_pypy
def test_roundtrip_with_dict():
    from pybind11_tests import PickleableWithDict

    p = PickleableWithDict("test_value")
    p.extra = 15
    p.dynamic = "Attribute"

    data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
    p2 = pickle.loads(data)
    if p2.value != p.value:
        raise AssertionError
    if p2.extra != p.extra:
        raise AssertionError
    if p2.dynamic != p.dynamic:
        raise AssertionError
