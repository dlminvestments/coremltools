import pytest

with pytest.suppress(ImportError):
    import numpy as np


@pytest.fixture(scope='function')
def arr():
    return np.array([[1, 2, 3], [4, 5, 6]], '<u2')


@pytest.requires_numpy
def test_array_attributes():
    from pybind11_tests.array import (
        ndim, shape, strides, writeable, size, itemsize, nbytes, owndata
    )

    a = np.array(0, 'f8')
    if ndim(a) != 0:
        raise AssertionError
    if not all(shape(a) == []):
        raise AssertionError
    if not all(strides(a) == []):
        raise AssertionError
    with pytest.raises(IndexError) as excinfo:
        shape(a, 0)
    if str(excinfo.value) != 'invalid axis: 0 (ndim = 0)':
        raise AssertionError
    with pytest.raises(IndexError) as excinfo:
        strides(a, 0)
    if str(excinfo.value) != 'invalid axis: 0 (ndim = 0)':
        raise AssertionError
    if not writeable(a):
        raise AssertionError
    if size(a) != 1:
        raise AssertionError
    if itemsize(a) != 8:
        raise AssertionError
    if nbytes(a) != 8:
        raise AssertionError
    if not owndata(a):
        raise AssertionError

    a = np.array([[1, 2, 3], [4, 5, 6]], 'u2').view()
    a.flags.writeable = False
    if ndim(a) != 2:
        raise AssertionError
    if not all(shape(a) == [2, 3]):
        raise AssertionError
    if shape(a, 0) != 2:
        raise AssertionError
    if shape(a, 1) != 3:
        raise AssertionError
    if not all(strides(a) == [6, 2]):
        raise AssertionError
    if strides(a, 0) != 6:
        raise AssertionError
    if strides(a, 1) != 2:
        raise AssertionError
    with pytest.raises(IndexError) as excinfo:
        shape(a, 2)
    if str(excinfo.value) != 'invalid axis: 2 (ndim = 2)':
        raise AssertionError
    with pytest.raises(IndexError) as excinfo:
        strides(a, 2)
    if str(excinfo.value) != 'invalid axis: 2 (ndim = 2)':
        raise AssertionError
    if writeable(a):
        raise AssertionError
    if size(a) != 6:
        raise AssertionError
    if itemsize(a) != 2:
        raise AssertionError
    if nbytes(a) != 12:
        raise AssertionError
    if owndata(a):
        raise AssertionError


@pytest.requires_numpy
@pytest.mark.parametrize('args, ret', [([], 0), ([0], 0), ([1], 3), ([0, 1], 1), ([1, 2], 5)])
def test_index_offset(arr, args, ret):
    from pybind11_tests.array import index_at, index_at_t, offset_at, offset_at_t
    if index_at(arr, *args) != ret:
        raise AssertionError
    if index_at_t(arr, *args) != ret:
        raise AssertionError
    if offset_at(arr, *args) != ret * arr.dtype.itemsize:
        raise AssertionError
    if offset_at_t(arr, *args) != ret * arr.dtype.itemsize:
        raise AssertionError


@pytest.requires_numpy
def test_dim_check_fail(arr):
    from pybind11_tests.array import (index_at, index_at_t, offset_at, offset_at_t, data, data_t,
                                      mutate_data, mutate_data_t)
    for func in (index_at, index_at_t, offset_at, offset_at_t, data, data_t,
                 mutate_data, mutate_data_t):
        with pytest.raises(IndexError) as excinfo:
            func(arr, 1, 2, 3)
        if str(excinfo.value) != 'too many indices for an array: 3 (ndim = 2)':
            raise AssertionError


@pytest.requires_numpy
@pytest.mark.parametrize('args, ret',
                         [([], [1, 2, 3, 4, 5, 6]),
                          ([1], [4, 5, 6]),
                          ([0, 1], [2, 3, 4, 5, 6]),
                          ([1, 2], [6])])
def test_data(arr, args, ret):
    from pybind11_tests.array import data, data_t
    if not all(data_t(arr, *args) == ret):
        raise AssertionError
    if not all(data(arr, *args)[::2] == ret):
        raise AssertionError
    if not all(data(arr, *args)[1::2] == 0):
        raise AssertionError


@pytest.requires_numpy
def test_mutate_readonly(arr):
    from pybind11_tests.array import mutate_data, mutate_data_t, mutate_at_t
    arr.flags.writeable = False
    for func, args in (mutate_data, ()), (mutate_data_t, ()), (mutate_at_t, (0, 0)):
        with pytest.raises(RuntimeError) as excinfo:
            func(arr, *args)
        if str(excinfo.value) != 'array is not writeable':
            raise AssertionError


@pytest.requires_numpy
@pytest.mark.parametrize('dim', [0, 1, 3])
def test_at_fail(arr, dim):
    from pybind11_tests.array import at_t, mutate_at_t
    for func in at_t, mutate_at_t:
        with pytest.raises(IndexError) as excinfo:
            func(arr, *([0] * dim))
        if str(excinfo.value) != 'index dimension mismatch: {} (ndim = 2)'.format(dim):
            raise AssertionError


@pytest.requires_numpy
def test_at(arr):
    from pybind11_tests.array import at_t, mutate_at_t

    if at_t(arr, 0, 2) != 3:
        raise AssertionError
    if at_t(arr, 1, 0) != 4:
        raise AssertionError

    if not all(mutate_at_t(arr, 0, 2).ravel() == [1, 2, 4, 4, 5, 6]):
        raise AssertionError
    if not all(mutate_at_t(arr, 1, 0).ravel() == [1, 2, 4, 5, 5, 6]):
        raise AssertionError


@pytest.requires_numpy
def test_mutate_data(arr):
    from pybind11_tests.array import mutate_data, mutate_data_t

    if not all(mutate_data(arr).ravel() == [2, 4, 6, 8, 10, 12]):
        raise AssertionError
    if not all(mutate_data(arr).ravel() == [4, 8, 12, 16, 20, 24]):
        raise AssertionError
    if not all(mutate_data(arr, 1).ravel() == [4, 8, 12, 32, 40, 48]):
        raise AssertionError
    if not all(mutate_data(arr, 0, 1).ravel() == [4, 16, 24, 64, 80, 96]):
        raise AssertionError
    if not all(mutate_data(arr, 1, 2).ravel() == [4, 16, 24, 64, 80, 192]):
        raise AssertionError

    if not all(mutate_data_t(arr).ravel() == [5, 17, 25, 65, 81, 193]):
        raise AssertionError
    if not all(mutate_data_t(arr).ravel() == [6, 18, 26, 66, 82, 194]):
        raise AssertionError
    if not all(mutate_data_t(arr, 1).ravel() == [6, 18, 26, 67, 83, 195]):
        raise AssertionError
    if not all(mutate_data_t(arr, 0, 1).ravel() == [6, 19, 27, 68, 84, 196]):
        raise AssertionError
    if not all(mutate_data_t(arr, 1, 2).ravel() == [6, 19, 27, 68, 84, 197]):
        raise AssertionError


@pytest.requires_numpy
def test_bounds_check(arr):
    from pybind11_tests.array import (index_at, index_at_t, data, data_t,
                                      mutate_data, mutate_data_t, at_t, mutate_at_t)
    funcs = (index_at, index_at_t, data, data_t,
             mutate_data, mutate_data_t, at_t, mutate_at_t)
    for func in funcs:
        with pytest.raises(IndexError) as excinfo:
            func(arr, 2, 0)
        if str(excinfo.value) != 'index 2 is out of bounds for axis 0 with size 2':
            raise AssertionError
        with pytest.raises(IndexError) as excinfo:
            func(arr, 0, 4)
        if str(excinfo.value) != 'index 4 is out of bounds for axis 1 with size 3':
            raise AssertionError


@pytest.requires_numpy
def test_make_c_f_array():
    from pybind11_tests.array import (
        make_c_array, make_f_array
    )
    if not make_c_array().flags.c_contiguous:
        raise AssertionError
    if make_c_array().flags.f_contiguous:
        raise AssertionError
    if not make_f_array().flags.f_contiguous:
        raise AssertionError
    if make_f_array().flags.c_contiguous:
        raise AssertionError


@pytest.requires_numpy
def test_wrap():
    from pybind11_tests.array import wrap

    def assert_references(a, b):
        if a is b:
            raise AssertionError
        if a.__array_interface__['data'][0] != b.__array_interface__['data'][0]:
            raise AssertionError
        if a.shape != b.shape:
            raise AssertionError
        if a.strides != b.strides:
            raise AssertionError
        if a.flags.c_contiguous != b.flags.c_contiguous:
            raise AssertionError
        if a.flags.f_contiguous != b.flags.f_contiguous:
            raise AssertionError
        if a.flags.writeable != b.flags.writeable:
            raise AssertionError
        if a.flags.aligned != b.flags.aligned:
            raise AssertionError
        if a.flags.updateifcopy != b.flags.updateifcopy:
            raise AssertionError
        if not np.all(a == b):
            raise AssertionError
        if b.flags.owndata:
            raise AssertionError
        if b.base is not a:
            raise AssertionError
        if a.flags.writeable and a.ndim == 2:
            a[0, 0] = 1234
            if b[0, 0] != 1234:
                raise AssertionError

    a1 = np.array([1, 2], dtype=np.int16)
    if not (a1.flags.owndata and a1.base is None):
        raise AssertionError
    a2 = wrap(a1)
    assert_references(a1, a2)

    a1 = np.array([[1, 2], [3, 4]], dtype=np.float32, order='F')
    if not (a1.flags.owndata and a1.base is None):
        raise AssertionError
    a2 = wrap(a1)
    assert_references(a1, a2)

    a1 = np.array([[1, 2], [3, 4]], dtype=np.float32, order='C')
    a1.flags.writeable = False
    a2 = wrap(a1)
    assert_references(a1, a2)

    a1 = np.random.random((4, 4, 4))
    a2 = wrap(a1)
    assert_references(a1, a2)

    a1 = a1.transpose()
    a2 = wrap(a1)
    assert_references(a1, a2)

    a1 = a1.diagonal()
    a2 = wrap(a1)
    assert_references(a1, a2)


@pytest.requires_numpy
def test_numpy_view(capture):
    from pybind11_tests.array import ArrayClass
    with capture:
        ac = ArrayClass()
        ac_view_1 = ac.numpy_view()
        ac_view_2 = ac.numpy_view()
        if not np.all(ac_view_1 == np.array([1, 2], dtype=np.int32)):
            raise AssertionError
        del ac
        pytest.gc_collect()
    if capture != """
        ArrayClass()
        ArrayClass::numpy_view()
        ArrayClass::numpy_view()
    """:
        raise AssertionError
    ac_view_1[0] = 4
    ac_view_1[1] = 3
    if ac_view_2[0] != 4:
        raise AssertionError
    if ac_view_2[1] != 3:
        raise AssertionError
    with capture:
        del ac_view_1
        del ac_view_2
        pytest.gc_collect()
        pytest.gc_collect()
    if capture != """
        ~ArrayClass()
    """:
        raise AssertionError


@pytest.unsupported_on_pypy
@pytest.requires_numpy
def test_cast_numpy_int64_to_uint64():
    from pybind11_tests.array import function_taking_uint64
    function_taking_uint64(123)
    function_taking_uint64(np.uint64(123))


@pytest.requires_numpy
def test_isinstance():
    from pybind11_tests.array import isinstance_untyped, isinstance_typed

    if not isinstance_untyped(np.array([1, 2, 3]), "not an array"):
        raise AssertionError
    if not isinstance_typed(np.array([1.0, 2.0, 3.0])):
        raise AssertionError


@pytest.requires_numpy
def test_constructors():
    from pybind11_tests.array import default_constructors, converting_constructors

    defaults = default_constructors()
    for a in defaults.values():
        if a.size != 0:
            raise AssertionError
    if defaults["array"].dtype != np.array([]).dtype:
        raise AssertionError
    if defaults["array_t<int32>"].dtype != np.int32:
        raise AssertionError
    if defaults["array_t<double>"].dtype != np.float64:
        raise AssertionError

    results = converting_constructors([1, 2, 3])
    for a in results.values():
        np.testing.assert_array_equal(a, [1, 2, 3])
    if results["array"].dtype != np.int_:
        raise AssertionError
    if results["array_t<int32>"].dtype != np.int32:
        raise AssertionError
    if results["array_t<double>"].dtype != np.float64:
        raise AssertionError
