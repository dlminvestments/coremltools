import pytest


def test_unscoped_enum():
    from pybind11_tests import UnscopedEnum, EOne

    if str(UnscopedEnum.EOne) != "UnscopedEnum.EOne":
        raise AssertionError
    if str(UnscopedEnum.ETwo) != "UnscopedEnum.ETwo":
        raise AssertionError
    if str(EOne) != "UnscopedEnum.EOne":
        raise AssertionError

    # no TypeError exception for unscoped enum ==/!= int comparisons
    y = UnscopedEnum.ETwo
    if y != 2:
        raise AssertionError
    if y == 3:
        raise AssertionError

    if int(UnscopedEnum.ETwo) != 2:
        raise AssertionError
    if str(UnscopedEnum(2)) != "UnscopedEnum.ETwo":
        raise AssertionError

    # order
    if UnscopedEnum.EOne >= UnscopedEnum.ETwo:
        raise AssertionError
    if UnscopedEnum.EOne >= 2:
        raise AssertionError
    if UnscopedEnum.ETwo <= UnscopedEnum.EOne:
        raise AssertionError
    if UnscopedEnum.ETwo <= 1:
        raise AssertionError
    if UnscopedEnum.ETwo > 2:
        raise AssertionError
    if UnscopedEnum.ETwo < 2:
        raise AssertionError
    if UnscopedEnum.EOne > UnscopedEnum.ETwo:
        raise AssertionError
    if UnscopedEnum.EOne > 2:
        raise AssertionError
    if UnscopedEnum.ETwo < UnscopedEnum.EOne:
        raise AssertionError
    if UnscopedEnum.ETwo < 1:
        raise AssertionError
    if (UnscopedEnum.ETwo < UnscopedEnum.EOne):
        raise AssertionError
    if (2 < UnscopedEnum.EOne):
        raise AssertionError


def test_scoped_enum():
    from pybind11_tests import ScopedEnum, test_scoped_enum

    if test_scoped_enum(ScopedEnum.Three) != "ScopedEnum::Three":
        raise AssertionError
    z = ScopedEnum.Two
    if test_scoped_enum(z) != "ScopedEnum::Two":
        raise AssertionError

    # expected TypeError exceptions for scoped enum ==/!= int comparisons
    with pytest.raises(TypeError):
        if z != 2:
            raise AssertionError
    with pytest.raises(TypeError):
        if z == 3:
            raise AssertionError

    # order
    if ScopedEnum.Two >= ScopedEnum.Three:
        raise AssertionError
    if ScopedEnum.Three <= ScopedEnum.Two:
        raise AssertionError
    if ScopedEnum.Two > ScopedEnum.Three:
        raise AssertionError
    if ScopedEnum.Two > ScopedEnum.Two:
        raise AssertionError
    if ScopedEnum.Two < ScopedEnum.Two:
        raise AssertionError
    if ScopedEnum.Three < ScopedEnum.Two:
        raise AssertionError


def test_implicit_conversion():
    from pybind11_tests import ClassWithUnscopedEnum

    if str(ClassWithUnscopedEnum.EMode.EFirstMode) != "EMode.EFirstMode":
        raise AssertionError
    if str(ClassWithUnscopedEnum.EFirstMode) != "EMode.EFirstMode":
        raise AssertionError

    f = ClassWithUnscopedEnum.test_function
    first = ClassWithUnscopedEnum.EFirstMode
    second = ClassWithUnscopedEnum.ESecondMode

    if f(first) != 1:
        raise AssertionError

    if f(first) != f(first):
        raise AssertionError
    if f(first) != f(first):
        raise AssertionError

    if f(first) == f(second):
        raise AssertionError
    if f(first) == f(second):
        raise AssertionError

    if f(first) != int(f(first)):
        raise AssertionError
    if f(first) != int(f(first)):
        raise AssertionError

    if f(first) == int(f(second)):
        raise AssertionError
    if f(first) == int(f(second)):
        raise AssertionError

    # noinspection PyDictCreation
    x = {f(first): 1, f(second): 2}
    x[f(first)] = 3
    x[f(second)] = 4
    # Hashing test
    if str(x) != "{EMode.EFirstMode: 3, EMode.ESecondMode: 4}":
        raise AssertionError


def test_binary_operators():
    from pybind11_tests import Flags

    if int(Flags.Read) != 4:
        raise AssertionError
    if int(Flags.Write) != 2:
        raise AssertionError
    if int(Flags.Execute) != 1:
        raise AssertionError
    if int(Flags.Read | Flags.Write | Flags.Execute) != 7:
        raise AssertionError
    if int(Flags.Read | Flags.Write) != 6:
        raise AssertionError
    if int(Flags.Read | Flags.Execute) != 5:
        raise AssertionError
    if int(Flags.Write | Flags.Execute) != 3:
        raise AssertionError
    if int(Flags.Write | 1) != 3:
        raise AssertionError

    state = Flags.Read | Flags.Write
    if (state & Flags.Read) == 0:
        raise AssertionError
    if (state & Flags.Write) == 0:
        raise AssertionError
    if (state & Flags.Execute) != 0:
        raise AssertionError
    if (state & 1) != 0:
        raise AssertionError

    state2 = ~state
    if state2 != -7:
        raise AssertionError
    if int(state ^ state2) != -1:
        raise AssertionError
