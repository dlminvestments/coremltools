import pytest


def isclose(a, b, rel_tol=1e-05, abs_tol=0.0):
    """Like math.isclose() from Python 3.5"""
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def allclose(a_list, b_list, rel_tol=1e-05, abs_tol=0.0):
    return all(isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol) for a, b in zip(a_list, b_list))


def test_generalized_iterators():
    from pybind11_tests import IntPairs

    if list(IntPairs([(1, 2), (3, 4), (0, 5)]).nonzero()) != [(1, 2), (3, 4)]:
        raise AssertionError
    if list(IntPairs([(1, 2), (2, 0), (0, 3), (4, 5)]).nonzero()) != [(1, 2)]:
        raise AssertionError
    if list(IntPairs([(0, 3), (1, 2), (3, 4)]).nonzero()) != []:
        raise AssertionError

    if list(IntPairs([(1, 2), (3, 4), (0, 5)]).nonzero_keys()) != [1, 3]:
        raise AssertionError
    if list(IntPairs([(1, 2), (2, 0), (0, 3), (4, 5)]).nonzero_keys()) != [1]:
        raise AssertionError
    if list(IntPairs([(0, 3), (1, 2), (3, 4)]).nonzero_keys()) != []:
        raise AssertionError


def test_sequence():
    from pybind11_tests import Sequence, ConstructorStats

    cstats = ConstructorStats.get(Sequence)

    s = Sequence(5)
    if cstats.values() != ['of size', '5']:
        raise AssertionError

    if "Sequence" not in repr(s):
        raise AssertionError
    if len(s) != 5:
        raise AssertionError
    if not (s[0] == 0 and s[3] == 0):
        raise AssertionError
    if 12.34 in s:
        raise AssertionError
    s[0], s[3] = 12.34, 56.78
    if 12.34 not in s:
        raise AssertionError
    if not (isclose(s[0], 12.34) and isclose(s[3], 56.78)):
        raise AssertionError

    rev = reversed(s)
    if cstats.values() != ['of size', '5']:
        raise AssertionError

    rev2 = s[::-1]
    if cstats.values() != ['of size', '5']:
        raise AssertionError

    expected = [0, 56.78, 0, 0, 12.34]
    if not allclose(rev, expected):
        raise AssertionError
    if not allclose(rev2, expected):
        raise AssertionError
    if rev != rev2:
        raise AssertionError

    rev[0::2] = Sequence([2.0, 2.0, 2.0])
    if cstats.values() != ['of size', '3', 'from std::vector']:
        raise AssertionError

    if not allclose(rev, [2, 56.78, 2, 0, 2]):
        raise AssertionError

    if cstats.alive() != 3:
        raise AssertionError
    del s
    if cstats.alive() != 2:
        raise AssertionError
    del rev
    if cstats.alive() != 1:
        raise AssertionError
    del rev2
    if cstats.alive() != 0:
        raise AssertionError

    if cstats.values() != []:
        raise AssertionError
    if cstats.default_constructions != 0:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    if cstats.move_constructions < 1:
        raise AssertionError
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError


def test_map_iterator():
    from pybind11_tests import StringMap

    m = StringMap({'hi': 'bye', 'black': 'white'})
    if m['hi'] != 'bye':
        raise AssertionError
    if len(m) != 2:
        raise AssertionError
    if m['black'] != 'white':
        raise AssertionError

    with pytest.raises(KeyError):
        if not m['orange']:
            raise AssertionError
    m['orange'] = 'banana'
    if m['orange'] != 'banana':
        raise AssertionError

    expected = {'hi': 'bye', 'black': 'white', 'orange': 'banana'}
    for k in m:
        if m[k] != expected[k]:
            raise AssertionError
    for k, v in m.items():
        if v != expected[k]:
            raise AssertionError
