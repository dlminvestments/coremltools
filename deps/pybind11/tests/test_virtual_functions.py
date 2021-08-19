import pytest
import pybind11_tests
from pybind11_tests import ConstructorStats


def test_override(capture, msg):
    from pybind11_tests import (ExampleVirt, runExampleVirt, runExampleVirtVirtual,
                                runExampleVirtBool)

    class ExtendedExampleVirt(ExampleVirt):
        def __init__(self, state):
            super(ExtendedExampleVirt, self).__init__(state + 1)
            self.data = "Hello world"

        def run(self, value):
            print('ExtendedExampleVirt::run(%i), calling parent..' % value)
            return super(ExtendedExampleVirt, self).run(value + 1)

        @staticmethod
        def run_bool():
            print('ExtendedExampleVirt::run_bool()')
            return False

        @staticmethod
        def get_string1():
            return "override1"

        def pure_virtual(self):
            print('ExtendedExampleVirt::pure_virtual(): %s' % self.data)

    class ExtendedExampleVirt2(ExtendedExampleVirt):
        def __init__(self, state):
            super(ExtendedExampleVirt2, self).__init__(state + 1)

        @staticmethod
        def get_string2():
            return "override2"

    ex12 = ExampleVirt(10)
    with capture:
        if runExampleVirt(ex12, 20) != 30:
            raise AssertionError
    if capture != """
        Original implementation of ExampleVirt::run(state=10, value=20, str1=default1, str2=default2)
    """:
        raise AssertionError

    with pytest.raises(RuntimeError) as excinfo:
        runExampleVirtVirtual(ex12)
    if msg(excinfo.value) != 'Tried to call pure virtual function "ExampleVirt::pure_virtual"':
        raise AssertionError

    ex12p = ExtendedExampleVirt(10)
    with capture:
        if runExampleVirt(ex12p, 20) != 32:
            raise AssertionError
    if capture != """
        ExtendedExampleVirt::run(20), calling parent..
        Original implementation of ExampleVirt::run(state=11, value=21, str1=override1, str2=default2)
    """:
        raise AssertionError
    with capture:
        if runExampleVirtBool(ex12p) is not False:
            raise AssertionError
    if capture != "ExtendedExampleVirt::run_bool()":
        raise AssertionError
    with capture:
        runExampleVirtVirtual(ex12p)
    if capture != "ExtendedExampleVirt::pure_virtual(): Hello world":
        raise AssertionError

    ex12p2 = ExtendedExampleVirt2(15)
    with capture:
        if runExampleVirt(ex12p2, 50) != 68:
            raise AssertionError
    if capture != """
        ExtendedExampleVirt::run(50), calling parent..
        Original implementation of ExampleVirt::run(state=17, value=51, str1=override1, str2=override2)
    """:
        raise AssertionError

    cstats = ConstructorStats.get(ExampleVirt)
    if cstats.alive() != 3:
        raise AssertionError
    del ex12, ex12p, ex12p2
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ['10', '11', '17']:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    if cstats.move_constructions < 0:
        raise AssertionError


def test_inheriting_repeat():
    from pybind11_tests import A_Repeat, B_Repeat, C_Repeat, D_Repeat, A_Tpl, B_Tpl, C_Tpl, D_Tpl

    class AR(A_Repeat):
        @staticmethod
        def unlucky_number():
            return 99

    class AT(A_Tpl):
        @staticmethod
        def unlucky_number():
            return 999

    obj = AR()
    if obj.say_something(3) != "hihihi":
        raise AssertionError
    if obj.unlucky_number() != 99:
        raise AssertionError
    if obj.say_everything() != "hi 99":
        raise AssertionError

    obj = AT()
    if obj.say_something(3) != "hihihi":
        raise AssertionError
    if obj.unlucky_number() != 999:
        raise AssertionError
    if obj.say_everything() != "hi 999":
        raise AssertionError

    for obj in [B_Repeat(), B_Tpl()]:
        if obj.say_something(3) != "B says hi 3 times":
            raise AssertionError
        if obj.unlucky_number() != 13:
            raise AssertionError
        if obj.lucky_number() != 7.0:
            raise AssertionError
        if obj.say_everything() != "B says hi 1 times 13":
            raise AssertionError

    for obj in [C_Repeat(), C_Tpl()]:
        if obj.say_something(3) != "B says hi 3 times":
            raise AssertionError
        if obj.unlucky_number() != 4444:
            raise AssertionError
        if obj.lucky_number() != 888.0:
            raise AssertionError
        if obj.say_everything() != "B says hi 1 times 4444":
            raise AssertionError

    class CR(C_Repeat):
        def lucky_number(self):
            return C_Repeat.lucky_number(self) + 1.25

    obj = CR()
    if obj.say_something(3) != "B says hi 3 times":
        raise AssertionError
    if obj.unlucky_number() != 4444:
        raise AssertionError
    if obj.lucky_number() != 889.25:
        raise AssertionError
    if obj.say_everything() != "B says hi 1 times 4444":
        raise AssertionError

    class CT(C_Tpl):
        pass

    obj = CT()
    if obj.say_something(3) != "B says hi 3 times":
        raise AssertionError
    if obj.unlucky_number() != 4444:
        raise AssertionError
    if obj.lucky_number() != 888.0:
        raise AssertionError
    if obj.say_everything() != "B says hi 1 times 4444":
        raise AssertionError

    class CCR(CR):
        def lucky_number(self):
            return CR.lucky_number(self) * 10

    obj = CCR()
    if obj.say_something(3) != "B says hi 3 times":
        raise AssertionError
    if obj.unlucky_number() != 4444:
        raise AssertionError
    if obj.lucky_number() != 8892.5:
        raise AssertionError
    if obj.say_everything() != "B says hi 1 times 4444":
        raise AssertionError

    class CCT(CT):
        def lucky_number(self):
            return CT.lucky_number(self) * 1000

    obj = CCT()
    if obj.say_something(3) != "B says hi 3 times":
        raise AssertionError
    if obj.unlucky_number() != 4444:
        raise AssertionError
    if obj.lucky_number() != 888000.0:
        raise AssertionError
    if obj.say_everything() != "B says hi 1 times 4444":
        raise AssertionError

    class DR(D_Repeat):
        @staticmethod
        def unlucky_number():
            return 123

        @staticmethod
        def lucky_number():
            return 42.0

    for obj in [D_Repeat(), D_Tpl()]:
        if obj.say_something(3) != "B says hi 3 times":
            raise AssertionError
        if obj.unlucky_number() != 4444:
            raise AssertionError
        if obj.lucky_number() != 888.0:
            raise AssertionError
        if obj.say_everything() != "B says hi 1 times 4444":
            raise AssertionError

    obj = DR()
    if obj.say_something(3) != "B says hi 3 times":
        raise AssertionError
    if obj.unlucky_number() != 123:
        raise AssertionError
    if obj.lucky_number() != 42.0:
        raise AssertionError
    if obj.say_everything() != "B says hi 1 times 123":
        raise AssertionError

    class DT(D_Tpl):
        @staticmethod
        def say_something(times):
            return "DT says:" + (' quack' * times)

        @staticmethod
        def unlucky_number():
            return 1234

        @staticmethod
        def lucky_number():
            return -4.25

    obj = DT()
    if obj.say_something(3) != "DT says: quack quack quack":
        raise AssertionError
    if obj.unlucky_number() != 1234:
        raise AssertionError
    if obj.lucky_number() != -4.25:
        raise AssertionError
    if obj.say_everything() != "DT says: quack 1234":
        raise AssertionError

    class DT2(DT):
        def say_something(self, times):
            return "DT2: " + ('QUACK' * times)

        def unlucky_number(self):
            return -3

    class BT(B_Tpl):
        @staticmethod
        def say_something(times):
            return "BT" * times

        @staticmethod
        def unlucky_number():
            return -7

        @staticmethod
        def lucky_number():
            return -1.375

    obj = BT()
    if obj.say_something(3) != "BTBTBT":
        raise AssertionError
    if obj.unlucky_number() != -7:
        raise AssertionError
    if obj.lucky_number() != -1.375:
        raise AssertionError
    if obj.say_everything() != "BT -7":
        raise AssertionError


# PyPy: Reference count > 1 causes call with noncopyable instance
# to fail in ncv1.print_nc()
@pytest.unsupported_on_pypy
@pytest.mark.skipif(not hasattr(pybind11_tests, 'NCVirt'),
                    reason="NCVirt test broken on ICPC")
def test_move_support():
    from pybind11_tests import NCVirt, NonCopyable, Movable

    class NCVirtExt(NCVirt):
        @staticmethod
        def get_noncopyable(a, b):
            # Constructs and returns a new instance:
            nc = NonCopyable(a * a, b * b)
            return nc

        def get_movable(self, a, b):
            # Return a referenced copy
            self.movable = Movable(a, b)
            return self.movable

    class NCVirtExt2(NCVirt):
        def get_noncopyable(self, a, b):
            # Keep a reference: this is going to throw an exception
            self.nc = NonCopyable(a, b)
            return self.nc

        @staticmethod
        def get_movable(a, b):
            # Return a new instance without storing it
            return Movable(a, b)

    ncv1 = NCVirtExt()
    if ncv1.print_nc(2, 3) != "36":
        raise AssertionError
    if ncv1.print_movable(4, 5) != "9":
        raise AssertionError
    ncv2 = NCVirtExt2()
    if ncv2.print_movable(7, 7) != "14":
        raise AssertionError
    # Don't check the exception message here because it differs under debug/non-debug mode
    with pytest.raises(RuntimeError):
        ncv2.print_nc(9, 9)

    nc_stats = ConstructorStats.get(NonCopyable)
    mv_stats = ConstructorStats.get(Movable)
    if nc_stats.alive() != 1:
        raise AssertionError
    if mv_stats.alive() != 1:
        raise AssertionError
    del ncv1, ncv2
    if nc_stats.alive() != 0:
        raise AssertionError
    if mv_stats.alive() != 0:
        raise AssertionError
    if nc_stats.values() != ['4', '9', '9', '9']:
        raise AssertionError
    if mv_stats.values() != ['4', '5', '7', '7']:
        raise AssertionError
    if nc_stats.copy_constructions != 0:
        raise AssertionError
    if mv_stats.copy_constructions != 1:
        raise AssertionError
    if nc_stats.move_constructions < 0:
        raise AssertionError
    if mv_stats.move_constructions < 0:
        raise AssertionError
