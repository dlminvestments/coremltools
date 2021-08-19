def test_operator_overloading():
    from pybind11_tests import Vector2, Vector, ConstructorStats

    v1 = Vector2(1, 2)
    v2 = Vector(3, -1)
    if str(v1) != "[1.000000, 2.000000]":
        raise AssertionError
    if str(v2) != "[3.000000, -1.000000]":
        raise AssertionError

    if str(v1 + v2) != "[4.000000, 1.000000]":
        raise AssertionError
    if str(v1 - v2) != "[-2.000000, 3.000000]":
        raise AssertionError
    if str(v1 - 8) != "[-7.000000, -6.000000]":
        raise AssertionError
    if str(v1 + 8) != "[9.000000, 10.000000]":
        raise AssertionError
    if str(v1 * 8) != "[8.000000, 16.000000]":
        raise AssertionError
    if str(v1 / 8) != "[0.125000, 0.250000]":
        raise AssertionError
    if str(8 - v1) != "[7.000000, 6.000000]":
        raise AssertionError
    if str(8 + v1) != "[9.000000, 10.000000]":
        raise AssertionError
    if str(8 * v1) != "[8.000000, 16.000000]":
        raise AssertionError
    if str(8 / v1) != "[8.000000, 4.000000]":
        raise AssertionError

    v1 += v2
    v1 *= 2
    if str(v1) != "[8.000000, 2.000000]":
        raise AssertionError

    cstats = ConstructorStats.get(Vector2)
    if cstats.alive() != 2:
        raise AssertionError
    del v1
    if cstats.alive() != 1:
        raise AssertionError
    del v2
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ['[1.000000, 2.000000]', '[3.000000, -1.000000]',
                               '[4.000000, 1.000000]', '[-2.000000, 3.000000]',
                               '[-7.000000, -6.000000]', '[9.000000, 10.000000]',
                               '[8.000000, 16.000000]', '[0.125000, 0.250000]',
                               '[7.000000, 6.000000]', '[9.000000, 10.000000]',
                               '[8.000000, 16.000000]', '[8.000000, 4.000000]']:
        raise AssertionError
    if cstats.default_constructions != 0:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    if cstats.move_constructions < 10:
        raise AssertionError
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError
