import pytest
from pybind11_tests import (kw_func0, kw_func1, kw_func2, kw_func3, kw_func4, args_function,
                            args_kwargs_function, kw_func_udl, kw_func_udl_z, KWClass)


def test_function_signatures(doc):
    if doc(kw_func0) != "kw_func0(arg0: int, arg1: int) -> str":
        raise AssertionError
    if doc(kw_func1) != "kw_func1(x: int, y: int) -> str":
        raise AssertionError
    if doc(kw_func2) != "kw_func2(x: int=100, y: int=200) -> str":
        raise AssertionError
    if doc(kw_func3) != "kw_func3(data: str='Hello world!') -> None":
        raise AssertionError
    if doc(kw_func4) != "kw_func4(myList: List[int]=[13, 17]) -> str":
        raise AssertionError
    if doc(kw_func_udl) != "kw_func_udl(x: int, y: int=300) -> str":
        raise AssertionError
    if doc(kw_func_udl_z) != "kw_func_udl_z(x: int, y: int=0) -> str":
        raise AssertionError
    if doc(args_function) != "args_function(*args) -> tuple":
        raise AssertionError
    if doc(args_kwargs_function) != "args_kwargs_function(*args, **kwargs) -> tuple":
        raise AssertionError
    if doc(KWClass.foo0) != "foo0(self: m.KWClass, arg0: int, arg1: float) -> None":
        raise AssertionError
    if doc(KWClass.foo1) != "foo1(self: m.KWClass, x: int, y: float) -> None":
        raise AssertionError


def test_named_arguments(msg):
    if kw_func0(5, 10) != "x=5, y=10":
        raise AssertionError

    if kw_func1(5, 10) != "x=5, y=10":
        raise AssertionError
    if kw_func1(5, y=10) != "x=5, y=10":
        raise AssertionError
    if kw_func1(y=10, x=5) != "x=5, y=10":
        raise AssertionError

    if kw_func2() != "x=100, y=200":
        raise AssertionError
    if kw_func2(5) != "x=5, y=200":
        raise AssertionError
    if kw_func2(x=5) != "x=5, y=200":
        raise AssertionError
    if kw_func2(y=10) != "x=100, y=10":
        raise AssertionError
    if kw_func2(5, 10) != "x=5, y=10":
        raise AssertionError
    if kw_func2(x=5, y=10) != "x=5, y=10":
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        # noinspection PyArgumentList
        kw_func2(x=5, y=10, z=12)
    if msg(excinfo.value) != """
        kw_func2(): incompatible function arguments. The following argument types are supported:
            1. (x: int=100, y: int=200) -> str

        Invoked with:
    """:
        raise AssertionError

    if kw_func4() != "{13 17}":
        raise AssertionError
    if kw_func4(myList=[1, 2, 3]) != "{1 2 3}":
        raise AssertionError

    if kw_func_udl(x=5, y=10) != "x=5, y=10":
        raise AssertionError
    if kw_func_udl_z(x=5) != "x=5, y=0":
        raise AssertionError


def test_arg_and_kwargs():
    args = 'arg1_value', 'arg2_value', 3
    if args_function(*args) != args:
        raise AssertionError

    args = 'a1', 'a2'
    kwargs = dict(arg3='a3', arg4=4)
    if args_kwargs_function(*args, **kwargs) != (args, kwargs):
        raise AssertionError


def test_mixed_args_and_kwargs(msg):
    from pybind11_tests import (mixed_plus_args, mixed_plus_kwargs, mixed_plus_args_kwargs,
                                mixed_plus_args_kwargs_defaults)
    mpa = mixed_plus_args
    mpk = mixed_plus_kwargs
    mpak = mixed_plus_args_kwargs
    mpakd = mixed_plus_args_kwargs_defaults

    if mpa(1, 2.5, 4, 99.5, None) != (1, 2.5, (4, 99.5, None)):
        raise AssertionError
    if mpa(1, 2.5) != (1, 2.5, ()):
        raise AssertionError
    with pytest.raises(TypeError) as excinfo:
        if not mpa(1):
            raise AssertionError
    if msg(excinfo.value) != """
        mixed_plus_args(): incompatible function arguments. The following argument types are supported:
            1. (arg0: int, arg1: float, *args) -> tuple

        Invoked with: 1
    """:
        raise AssertionError
    with pytest.raises(TypeError) as excinfo:
        if not mpa():
            raise AssertionError
    if msg(excinfo.value) != """
        mixed_plus_args(): incompatible function arguments. The following argument types are supported:
            1. (arg0: int, arg1: float, *args) -> tuple

        Invoked with:
    """:
        raise AssertionError

    if mpk(-2, 3.5, pi=3.14159, e=2.71828) != (-2, 3.5, {'e': 2.71828, 'pi': 3.14159}):
        raise AssertionError
    if mpak(7, 7.7, 7.77, 7.777, 7.7777, minusseven=-7) != (
        7, 7.7, (7.77, 7.777, 7.7777), {'minusseven': -7}):
        raise AssertionError
    if mpakd() != (1, 3.14159, (), {}):
        raise AssertionError
    if mpakd(3) != (3, 3.14159, (), {}):
        raise AssertionError
    if mpakd(j=2.71828) != (1, 2.71828, (), {}):
        raise AssertionError
    if mpakd(k=42) != (1, 3.14159, (), {'k': 42}):
        raise AssertionError
    if mpakd(1, 1, 2, 3, 5, 8, then=13, followedby=21) != (
        1, 1, (2, 3, 5, 8), {'then': 13, 'followedby': 21}):
        raise AssertionError
    # Arguments specified both positionally and via kwargs is an error:
    with pytest.raises(TypeError) as excinfo:
        if not mpakd(1, i=1):
            raise AssertionError
    if msg(excinfo.value) != """
        mixed_plus_args_kwargs_defaults(): got multiple values for argument 'i'
    """:
        raise AssertionError
    with pytest.raises(TypeError) as excinfo:
        if not mpakd(1, 2, j=1):
            raise AssertionError
    if msg(excinfo.value) != """
        mixed_plus_args_kwargs_defaults(): got multiple values for argument 'j'
    """:
        raise AssertionError
