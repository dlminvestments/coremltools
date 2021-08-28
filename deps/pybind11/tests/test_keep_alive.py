import pytest


def test_keep_alive_argument(capture):
    from pybind11_tests import Parent, Child

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.addChild(Child())
        pytest.gc_collect()
    if capture != """
        Allocating child.
        Releasing child.
    """:
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != "Releasing parent.":
        raise AssertionError

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.addChildKeepAlive(Child())
        pytest.gc_collect()
    if capture != "Allocating child.":
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != """
        Releasing parent.
        Releasing child.
    """:
        raise AssertionError


def test_keep_alive_return_value(capture):
    from pybind11_tests import Parent

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.returnChild()
        pytest.gc_collect()
    if capture != """
        Allocating child.
        Releasing child.
    """:
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != "Releasing parent.":
        raise AssertionError

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.returnChildKeepAlive()
        pytest.gc_collect()
    if capture != "Allocating child.":
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != """
        Releasing parent.
        Releasing child.
    """:
        raise AssertionError


def test_return_none(capture):
    from pybind11_tests import Parent

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.returnNullChildKeepAliveChild()
        pytest.gc_collect()
    if capture != "":
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != "Releasing parent.":
        raise AssertionError

    with capture:
        p = Parent()
    if capture != "Allocating parent.":
        raise AssertionError
    with capture:
        p.returnNullChildKeepAliveParent()
        pytest.gc_collect()
    if capture != "":
        raise AssertionError
    with capture:
        del p
        pytest.gc_collect()
    if capture != "Releasing parent.":
        raise AssertionError
