import pytest
from pybind11_tests import ExampleMandA, ConstructorStats


def test_methods_and_attributes():
    instance1 = ExampleMandA()
    instance2 = ExampleMandA(32)

    instance1.add1(instance2)
    instance1.add2(instance2)
    instance1.add3(instance2)
    instance1.add4(instance2)
    instance1.add5(instance2)
    instance1.add6(32)
    instance1.add7(32)
    instance1.add8(32)
    instance1.add9(32)
    instance1.add10(32)

    if str(instance1) != "ExampleMandA[value=320]":
        raise AssertionError
    if str(instance2) != "ExampleMandA[value=32]":
        raise AssertionError
    if str(instance1.self1()) != "ExampleMandA[value=320]":
        raise AssertionError
    if str(instance1.self2()) != "ExampleMandA[value=320]":
        raise AssertionError
    if str(instance1.self3()) != "ExampleMandA[value=320]":
        raise AssertionError
    if str(instance1.self4()) != "ExampleMandA[value=320]":
        raise AssertionError
    if str(instance1.self5()) != "ExampleMandA[value=320]":
        raise AssertionError

    if instance1.internal1() != 320:
        raise AssertionError
    if instance1.internal2() != 320:
        raise AssertionError
    if instance1.internal3() != 320:
        raise AssertionError
    if instance1.internal4() != 320:
        raise AssertionError
    if instance1.internal5() != 320:
        raise AssertionError

    if instance1.overloaded(1, 1.0) != "(int, float)":
        raise AssertionError
    if instance1.overloaded(2.0, 2) != "(float, int)":
        raise AssertionError
    if instance1.overloaded(3,   3) != "(int, int)":
        raise AssertionError
    if instance1.overloaded(4., 4.) != "(float, float)":
        raise AssertionError
    if instance1.overloaded_const(5, 5.0) != "(int, float) const":
        raise AssertionError
    if instance1.overloaded_const(6.0, 6) != "(float, int) const":
        raise AssertionError
    if instance1.overloaded_const(7,   7) != "(int, int) const":
        raise AssertionError
    if instance1.overloaded_const(8., 8.) != "(float, float) const":
        raise AssertionError
    if instance1.overloaded_float(1, 1) != "(float, float)":
        raise AssertionError
    if instance1.overloaded_float(1, 1.) != "(float, float)":
        raise AssertionError
    if instance1.overloaded_float(1., 1) != "(float, float)":
        raise AssertionError
    if instance1.overloaded_float(1., 1.) != "(float, float)":
        raise AssertionError

    if instance1.value != 320:
        raise AssertionError
    instance1.value = 100
    if str(instance1) != "ExampleMandA[value=100]":
        raise AssertionError

    cstats = ConstructorStats.get(ExampleMandA)
    if cstats.alive() != 2:
        raise AssertionError
    del instance1, instance2
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ["32"]:
        raise AssertionError
    if cstats.default_constructions != 1:
        raise AssertionError
    if cstats.copy_constructions != 3:
        raise AssertionError
    if cstats.move_constructions < 1:
        raise AssertionError
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError


def test_properties():
    from pybind11_tests import TestProperties

    instance = TestProperties()

    if instance.def_readonly != 1:
        raise AssertionError
    with pytest.raises(AttributeError):
        instance.def_readonly = 2

    instance.def_readwrite = 2
    if instance.def_readwrite != 2:
        raise AssertionError

    if instance.def_property_readonly != 2:
        raise AssertionError
    with pytest.raises(AttributeError):
        instance.def_property_readonly = 3

    instance.def_property = 3
    if instance.def_property != 3:
        raise AssertionError


def test_static_properties():
    from pybind11_tests import TestProperties as Type

    if Type.def_readonly_static != 1:
        raise AssertionError
    with pytest.raises(AttributeError):
        Type.def_readonly_static = 2

    Type.def_readwrite_static = 2
    if Type.def_readwrite_static != 2:
        raise AssertionError

    if Type.def_property_readonly_static != 2:
        raise AssertionError
    with pytest.raises(AttributeError):
        Type.def_property_readonly_static = 3

    Type.def_property_static = 3
    if Type.def_property_static != 3:
        raise AssertionError


@pytest.mark.parametrize("access", ["ro", "rw", "static_ro", "static_rw"])
def test_property_return_value_policies(access):
    from pybind11_tests import TestPropRVP

    if not access.startswith("static"):
        obj = TestPropRVP()
    else:
        obj = TestPropRVP

    ref = getattr(obj, access + "_ref")
    if ref.value != 1:
        raise AssertionError
    ref.value = 2
    if getattr(obj, access + "_ref").value != 2:
        raise AssertionError
    ref.value = 1  # restore original value for static properties

    copy = getattr(obj, access + "_copy")
    if copy.value != 1:
        raise AssertionError
    copy.value = 2
    if getattr(obj, access + "_copy").value != 1:
        raise AssertionError

    copy = getattr(obj, access + "_func")
    if copy.value != 1:
        raise AssertionError
    copy.value = 2
    if getattr(obj, access + "_func").value != 1:
        raise AssertionError


def test_property_rvalue_policy():
    """When returning an rvalue, the return value policy is automatically changed from
    `reference(_internal)` to `move`. The following would not work otherwise.
    """
    from pybind11_tests import TestPropRVP

    instance = TestPropRVP()
    o = instance.rvalue
    if o.value != 1:
        raise AssertionError


def test_property_rvalue_policy_static():
    """When returning an rvalue, the return value policy is automatically changed from
    `reference(_internal)` to `move`. The following would not work otherwise.
    """
    from pybind11_tests import TestPropRVP
    o = TestPropRVP.static_rvalue
    if o.value != 1:
        raise AssertionError


# https://bitbucket.org/pypy/pypy/issues/2447
@pytest.unsupported_on_pypy
def test_dynamic_attributes():
    from pybind11_tests import DynamicClass, CppDerivedDynamicClass

    instance = DynamicClass()
    if hasattr(instance, "foo"):
        raise AssertionError
    if "foo" in dir(instance):
        raise AssertionError

    # Dynamically add attribute
    instance.foo = 42
    if not hasattr(instance, "foo"):
        raise AssertionError
    if instance.foo != 42:
        raise AssertionError
    if "foo" not in dir(instance):
        raise AssertionError

    # __dict__ should be accessible and replaceable
    if "foo" not in instance.__dict__:
        raise AssertionError
    instance.__dict__ = {"bar": True}
    if hasattr(instance, "foo"):
        raise AssertionError
    if not hasattr(instance, "bar"):
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        instance.__dict__ = []
    if str(excinfo.value) != "__dict__ must be set to a dictionary, not a 'list'":
        raise AssertionError

    cstats = ConstructorStats.get(DynamicClass)
    if cstats.alive() != 1:
        raise AssertionError
    del instance
    if cstats.alive() != 0:
        raise AssertionError

    # Derived classes should work as well
    class PythonDerivedDynamicClass(DynamicClass):
        pass

    for cls in CppDerivedDynamicClass, PythonDerivedDynamicClass:
        derived = cls()
        derived.foobar = 100
        if derived.foobar != 100:
            raise AssertionError

        if cstats.alive() != 1:
            raise AssertionError
        del derived
        if cstats.alive() != 0:
            raise AssertionError


# https://bitbucket.org/pypy/pypy/issues/2447
@pytest.unsupported_on_pypy
def test_cyclic_gc():
    from pybind11_tests import DynamicClass

    # One object references itself
    instance = DynamicClass()
    instance.circular_reference = instance

    cstats = ConstructorStats.get(DynamicClass)
    if cstats.alive() != 1:
        raise AssertionError
    del instance
    if cstats.alive() != 0:
        raise AssertionError

    # Two object reference each other
    i1 = DynamicClass()
    i2 = DynamicClass()
    i1.cycle = i2
    i2.cycle = i1

    if cstats.alive() != 2:
        raise AssertionError
    del i1, i2
    if cstats.alive() != 0:
        raise AssertionError


def test_noconvert_args(msg):
    from pybind11_tests import ArgInspector, arg_inspect_func, floats_only, floats_preferred

    a = ArgInspector()
    if msg(a.f("hi")) != """
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = hi
    """:
        raise AssertionError
    if msg(a.g("this is a", "this is b")) != """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        13
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = (default arg inspector 2)
    """:
        raise AssertionError
    if msg(a.g("this is a", "this is b", 42)) != """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        42
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = (default arg inspector 2)
    """:
        raise AssertionError
    if msg(a.g("this is a", "this is b", 42, "this is d")) != """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        42
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = this is d
    """:
        raise AssertionError
    if (a.h("arg 1") != "loading ArgInspector2 argument WITHOUT conversion allowed.  Argument value = arg 1"):
        raise AssertionError
    if msg(arg_inspect_func("A1", "A2")) != """
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = A1
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = A2
    """:
        raise AssertionError

    if floats_preferred(4) != 2.0:
        raise AssertionError
    if floats_only(4.0) != 2.0:
        raise AssertionError
    with pytest.raises(TypeError) as excinfo:
        floats_only(4)
    if msg(excinfo.value) != """
        floats_only(): incompatible function arguments. The following argument types are supported:
            1. (f: float) -> float

        Invoked with: 4
    """:
        raise AssertionError


def test_bad_arg_default(msg):
    from pybind11_tests import debug_enabled, bad_arg_def_named, bad_arg_def_unnamed

    with pytest.raises(RuntimeError) as excinfo:
        bad_arg_def_named()
    if msg(excinfo.value) != (
        "arg(): could not convert default argument 'a: NotRegistered' in function 'should_fail' "
        "into a Python object (type not registered yet?)"
        if debug_enabled else
        "arg(): could not convert default argument into a Python object (type not registered "
        "yet?). Compile in debug mode for more information."
    ):
        raise AssertionError

    with pytest.raises(RuntimeError) as excinfo:
        bad_arg_def_unnamed()
    if msg(excinfo.value) != (
        "arg(): could not convert default argument 'NotRegistered' in function 'should_fail' "
        "into a Python object (type not registered yet?)"
        if debug_enabled else
        "arg(): could not convert default argument into a Python object (type not registered "
        "yet?). Compile in debug mode for more information."
    ):
        raise AssertionError
