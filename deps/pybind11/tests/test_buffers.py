import pytest
from pybind11_tests import Matrix, ConstructorStats

with pytest.suppress(ImportError):
    import numpy as np


@pytest.requires_numpy
def test_from_python():
    with pytest.raises(RuntimeError) as excinfo:
        Matrix(np.array([1, 2, 3]))  # trying to assign a 1D array
    if str(excinfo.value) != "Incompatible buffer format!":
        raise AssertionError

    m3 = np.array([[1, 2, 3], [4, 5, 6]]).astype(np.float32)
    m4 = Matrix(m3)

    for i in range(m4.rows()):
        for j in range(m4.cols()):
            if m3[i, j] != m4[i, j]:
                raise AssertionError

    cstats = ConstructorStats.get(Matrix)
    if cstats.alive() != 1:
        raise AssertionError
    del m3, m4
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ["2x3 matrix"]:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0  # Don't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError


# PyPy: Memory leak in the "np.array(m, copy=False)" call
# https://bitbucket.org/pypy/pypy/issues/2444
@pytest.unsupported_on_pypy
@pytest.requires_numpy
def test_to_python():
    m = Matrix(5, 5)

    if m[2, 3] != 0:
        raise AssertionError
    m[2, 3] = 4
    if m[2, 3] != 4:
        raise AssertionError

    m2 = np.array(m, copy=False)
    if m2.shape != (5, 5):
        raise AssertionError
    if abs(m2).sum() != 4:
        raise AssertionError
    if m2[2, 3] != 4:
        raise AssertionError
    m2[2, 3] = 5
    if m2[2, 3] != 5:
        raise AssertionError

    cstats = ConstructorStats.get(Matrix)
    if cstats.alive() != 1:
        raise AssertionError
    del m
    pytest.gc_collect()
    if cstats.alive() != 1:
        raise AssertionError
    del m2  # holds an m reference
    pytest.gc_collect()
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ["5x5 matrix"]:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0  # Don't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError
