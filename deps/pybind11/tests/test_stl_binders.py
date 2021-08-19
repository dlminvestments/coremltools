def test_vector_int():
    from pybind11_tests import VectorInt

    v_int = VectorInt([0, 0])
    if len(v_int) != 2:
        raise AssertionError
    if bool(v_int) is not True:
        raise AssertionError

    v_int2 = VectorInt([0, 0])
    if v_int != v_int2:
        raise AssertionError
    v_int2[1] = 1
    if v_int == v_int2:
        raise AssertionError

    v_int2.append(2)
    v_int2.append(3)
    v_int2.insert(0, 1)
    v_int2.insert(0, 2)
    v_int2.insert(0, 3)
    if str(v_int2) != "VectorInt[3, 2, 1, 0, 1, 2, 3]":
        raise AssertionError

    v_int.append(99)
    v_int2[2:-2] = v_int
    if v_int2 != VectorInt([3, 2, 0, 0, 99, 2, 3]):
        raise AssertionError
    del v_int2[1:3]
    if v_int2 != VectorInt([3, 0, 99, 2, 3]):
        raise AssertionError
    del v_int2[0]
    if v_int2 != VectorInt([0, 99, 2, 3]):
        raise AssertionError


def test_vector_custom():
    from pybind11_tests import El, VectorEl, VectorVectorEl

    v_a = VectorEl()
    v_a.append(El(1))
    v_a.append(El(2))
    if str(v_a) != "VectorEl[El{1}, El{2}]":
        raise AssertionError

    vv_a = VectorVectorEl()
    vv_a.append(v_a)
    vv_b = vv_a[0]
    if str(vv_b) != "VectorEl[El{1}, El{2}]":
        raise AssertionError


def test_vector_bool():
    from pybind11_tests import VectorBool

    vv_c = VectorBool()
    for i in range(10):
        vv_c.append(i % 2 == 0)
    for i in range(10):
        if vv_c[i] != (i % 2 == 0):
            raise AssertionError
    if str(vv_c) != "VectorBool[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]":
        raise AssertionError


def test_map_string_double():
    from pybind11_tests import MapStringDouble, UnorderedMapStringDouble

    m = MapStringDouble()
    m['a'] = 1
    m['b'] = 2.5

    if list(m) != ['a', 'b']:
        raise AssertionError
    if list(m.items()) != [('a', 1), ('b', 2.5)]:
        raise AssertionError
    if str(m) != "MapStringDouble{a: 1, b: 2.5}":
        raise AssertionError

    um = UnorderedMapStringDouble()
    um['ua'] = 1.1
    um['ub'] = 2.6

    if sorted(list(um)) != ['ua', 'ub']:
        raise AssertionError
    if sorted(list(um.items())) != [('ua', 1.1), ('ub', 2.6)]:
        raise AssertionError
    if "UnorderedMapStringDouble" not in str(um):
        raise AssertionError


def test_map_string_double_const():
    from pybind11_tests import MapStringDoubleConst, UnorderedMapStringDoubleConst

    mc = MapStringDoubleConst()
    mc['a'] = 10
    mc['b'] = 20.5
    if str(mc) != "MapStringDoubleConst{a: 10, b: 20.5}":
        raise AssertionError

    umc = UnorderedMapStringDoubleConst()
    umc['a'] = 11
    umc['b'] = 21.5

    str(umc)


def test_noncopyable_vector():
    from pybind11_tests import get_vnc

    vnc = get_vnc(5)
    for i in range(0, 5):
        if vnc[i].value != i + 1:
            raise AssertionError

    for i, j in enumerate(vnc, start=1):
        if j.value != i:
            raise AssertionError


def test_noncopyable_deque():
    from pybind11_tests import get_dnc

    dnc = get_dnc(5)
    for i in range(0, 5):
        if dnc[i].value != i + 1:
            raise AssertionError

    i = 1
    for j in dnc:
        if (j.value != i):
            raise AssertionError
        i += 1


def test_noncopyable_map():
    from pybind11_tests import get_mnc

    mnc = get_mnc(5)
    for i in range(1, 6):
        if mnc[i].value != 10 * i:
            raise AssertionError

    vsum = 0
    for k, v in mnc.items():
        if v.value != 10 * k:
            raise AssertionError
        vsum += v.value

    if vsum != 150:
        raise AssertionError


def test_noncopyable_unordered_map():
    from pybind11_tests import get_umnc

    mnc = get_umnc(5)
    for i in range(1, 6):
        if mnc[i].value != 10 * i:
            raise AssertionError

    vsum = 0
    for k, v in mnc.items():
        if v.value != 10 * k:
            raise AssertionError
        vsum += v.value

    if vsum != 150:
        raise AssertionError
