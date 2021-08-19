# Python < 3 needs this: coding=utf-8
import pytest

from pybind11_tests import ExamplePythonTypes, ConstructorStats, has_optional, has_exp_optional


def test_repr():
    # In Python 3.3+, repr() accesses __qualname__
    if "ExamplePythonTypes__Meta" not in repr(type(ExamplePythonTypes)):
        raise AssertionError
    if "ExamplePythonTypes" not in repr(ExamplePythonTypes):
        raise AssertionError


def test_static():
    ExamplePythonTypes.value = 15
    if ExamplePythonTypes.value != 15:
        raise AssertionError
    if ExamplePythonTypes.value2 != 5:
        raise AssertionError

    with pytest.raises(AttributeError) as excinfo:
        ExamplePythonTypes.value2 = 15
    if str(excinfo.value) != "can't set attribute":
        raise AssertionError


def test_instance(capture):
    with pytest.raises(TypeError) as excinfo:
        ExamplePythonTypes()
    if str(excinfo.value) != "pybind11_tests.ExamplePythonTypes: No constructor defined!":
        raise AssertionError

    instance = ExamplePythonTypes.new_instance()

    with capture:
        dict_result = instance.get_dict()
        dict_result['key2'] = 'value2'
        instance.print_dict(dict_result)
    if capture.unordered != """
        key: key, value=value
        key: key2, value=value2
    """:
        raise AssertionError
    with capture:
        dict_result = instance.get_dict_2()
        dict_result['key2'] = 'value2'
        instance.print_dict_2(dict_result)
    if capture.unordered != """
        key: key, value=value
        key: key2, value=value2
    """:
        raise AssertionError
    with capture:
        set_result = instance.get_set()
        set_result.add('key4')
        instance.print_set(set_result)
    if capture.unordered != """
        key: key1
        key: key2
        key: key3
        key: key4
    """:
        raise AssertionError
    with capture:
        set_result = instance.get_set2()
        set_result.add('key3')
        instance.print_set_2(set_result)
    if capture.unordered != """
        key: key1
        key: key2
        key: key3
    """:
        raise AssertionError
    with capture:
        list_result = instance.get_list()
        list_result.append('value2')
        instance.print_list(list_result)
    if capture.unordered != """
        Entry at position 0: value
        list item 0: overwritten
        list item 1: value2
    """:
        raise AssertionError
    with capture:
        list_result = instance.get_list_2()
        list_result.append('value2')
        instance.print_list_2(list_result)
    if capture.unordered != """
        list item 0: value
        list item 1: value2
    """:
        raise AssertionError
    with capture:
        list_result = instance.get_list_2()
        list_result.append('value2')
        instance.print_list_2(tuple(list_result))
    if capture.unordered != """
        list item 0: value
        list item 1: value2
    """:
        raise AssertionError
    array_result = instance.get_array()
    if array_result != ['array entry 1', 'array entry 2']:
        raise AssertionError
    with capture:
        instance.print_array(array_result)
    if capture.unordered != """
        array item 0: array entry 1
        array item 1: array entry 2
    """:
        raise AssertionError
    varray_result = instance.get_valarray()
    if varray_result != [1, 4, 9]:
        raise AssertionError
    with capture:
        instance.print_valarray(varray_result)
    if capture.unordered != """
        valarray item 0: 1
        valarray item 1: 4
        valarray item 2: 9
    """:
        raise AssertionError
    with pytest.raises(RuntimeError) as excinfo:
        instance.throw_exception()
    if str(excinfo.value) != "This exception was intentionally thrown.":
        raise AssertionError

    if instance.pair_passthrough((True, "test")) != ("test", True):
        raise AssertionError
    if instance.tuple_passthrough((True, "test", 5)) != (5, "test", True):
        raise AssertionError
    # Any sequence can be cast to a std::pair or std::tuple
    if instance.pair_passthrough([True, "test"]) != ("test", True):
        raise AssertionError
    if instance.tuple_passthrough([True, "test", 5]) != (5, "test", True):
        raise AssertionError

    if instance.get_bytes_from_string().decode() != "foo":
        raise AssertionError
    if instance.get_bytes_from_str().decode() != "bar":
        raise AssertionError
    if instance.get_str_from_string().encode().decode() != "baz":
        raise AssertionError
    if instance.get_str_from_bytes().encode().decode() != "boo":
        raise AssertionError

    class A(object):
        def __str__(self):
            return "this is a str"

        def __repr__(self):
            return "this is a repr"

    with capture:
        instance.test_print(A())
    if capture != """
        this is a str
        this is a repr
    """:
        raise AssertionError

    cstats = ConstructorStats.get(ExamplePythonTypes)
    if cstats.alive() != 1:
        raise AssertionError
    del instance
    if cstats.alive() != 0:
        raise AssertionError


# PyPy does not seem to propagate the tp_docs field at the moment
def test_class_docs(doc):
    if doc(ExamplePythonTypes) != "Example 2 documentation":
        raise AssertionError


def test_method_docs(doc):
    if doc(ExamplePythonTypes.get_dict) != """
        get_dict(self: m.ExamplePythonTypes) -> dict

        Return a Python dictionary
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_dict_2) != """
        get_dict_2(self: m.ExamplePythonTypes) -> Dict[str, str]

        Return a C++ dictionary
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_list) != """
        get_list(self: m.ExamplePythonTypes) -> list

        Return a Python list
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_list_2) != """
        get_list_2(self: m.ExamplePythonTypes) -> List[str]

        Return a C++ list
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_dict) != """
        get_dict(self: m.ExamplePythonTypes) -> dict

        Return a Python dictionary
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_set) != """
        get_set(self: m.ExamplePythonTypes) -> set

        Return a Python set
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_set2) != """
        get_set2(self: m.ExamplePythonTypes) -> Set[str]

        Return a C++ set
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_array) != """
        get_array(self: m.ExamplePythonTypes) -> List[str[2]]

        Return a C++ array
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.get_valarray) != """
        get_valarray(self: m.ExamplePythonTypes) -> List[int]

        Return a C++ valarray
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_dict) != """
        print_dict(self: m.ExamplePythonTypes, arg0: dict) -> None

        Print entries of a Python dictionary
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_dict_2) != """
        print_dict_2(self: m.ExamplePythonTypes, arg0: Dict[str, str]) -> None

        Print entries of a C++ dictionary
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_set) != """
        print_set(self: m.ExamplePythonTypes, arg0: set) -> None

        Print entries of a Python set
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_set_2) != """
        print_set_2(self: m.ExamplePythonTypes, arg0: Set[str]) -> None

        Print entries of a C++ set
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_list) != """
        print_list(self: m.ExamplePythonTypes, arg0: list) -> None

        Print entries of a Python list
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_list_2) != """
        print_list_2(self: m.ExamplePythonTypes, arg0: List[str]) -> None

        Print entries of a C++ list
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.print_array) != """
        print_array(self: m.ExamplePythonTypes, arg0: List[str[2]]) -> None

        Print entries of a C++ array
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.pair_passthrough) != """
        pair_passthrough(self: m.ExamplePythonTypes, arg0: Tuple[bool, str]) -> Tuple[str, bool]

        Return a pair in reversed order
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.tuple_passthrough) != """
        tuple_passthrough(self: m.ExamplePythonTypes, arg0: Tuple[bool, str, int]) -> Tuple[int, str, bool]

        Return a triple in reversed order
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.throw_exception) != """
        throw_exception(self: m.ExamplePythonTypes) -> None

        Throw an exception
    """:
        raise AssertionError
    if doc(ExamplePythonTypes.new_instance) != """
        new_instance() -> m.ExamplePythonTypes

        Return an instance
    """:
        raise AssertionError


def test_module():
    import pybind11_tests

    if pybind11_tests.__name__ != "pybind11_tests":
        raise AssertionError
    if ExamplePythonTypes.__name__ != "ExamplePythonTypes":
        raise AssertionError
    if ExamplePythonTypes.__module__ != "pybind11_tests":
        raise AssertionError
    if ExamplePythonTypes.get_set.__name__ != "get_set":
        raise AssertionError
    if ExamplePythonTypes.get_set.__module__ != "pybind11_tests":
        raise AssertionError


def test_print(capture):
    from pybind11_tests import test_print_function

    with capture:
        test_print_function()
    if capture != """
        Hello, World!
        1 2.0 three True -- multiple args
        *args-and-a-custom-separator
        no new line here -- next print
        flush
        py::print + str.format = this
    """:
        raise AssertionError
    if capture.stderr != "this goes to stderr":
        raise AssertionError


def test_str_api():
    from pybind11_tests import test_str_format

    s1, s2 = test_str_format()
    if s1 != "1 + 2 = 3":
        raise AssertionError
    if s1 != s2:
        raise AssertionError


def test_dict_api():
    from pybind11_tests import test_dict_keyword_constructor

    if test_dict_keyword_constructor() != {"x": 1, "y": 2, "z": 3}:
        raise AssertionError


def test_accessors():
    from pybind11_tests import test_accessor_api, test_tuple_accessor, test_accessor_assignment

    class SubTestObject:
        attr_obj = 1
        attr_char = 2

    class TestObject:
        basic_attr = 1
        begin_end = [1, 2, 3]
        d = {"operator[object]": 1, "operator[char *]": 2}
        sub = SubTestObject()

        def func(self, x, *args):
            return self.basic_attr + x + sum(args)

    d = test_accessor_api(TestObject())
    if d["basic_attr"] != 1:
        raise AssertionError
    if d["begin_end"] != [1, 2, 3]:
        raise AssertionError
    if d["operator[object]"] != 1:
        raise AssertionError
    if d["operator[char *]"] != 2:
        raise AssertionError
    if d["attr(object)"] != 1:
        raise AssertionError
    if d["attr(char *)"] != 2:
        raise AssertionError
    if d["missing_attr_ptr"] != "raised":
        raise AssertionError
    if d["missing_attr_chain"] != "raised":
        raise AssertionError
    if d["is_none"] is not False:
        raise AssertionError
    if d["operator()"] != 2:
        raise AssertionError
    if d["operator*"] != 7:
        raise AssertionError

    if test_tuple_accessor(tuple()) != (0, 1, 2):
        raise AssertionError

    d = test_accessor_assignment()
    if d["get"] != 0:
        raise AssertionError
    if d["deferred_get"] != 0:
        raise AssertionError
    if d["set"] != 1:
        raise AssertionError
    if d["deferred_set"] != 1:
        raise AssertionError
    if d["var"] != 99:
        raise AssertionError


@pytest.mark.skipif(not has_optional, reason='no <optional>')
def test_optional():
    from pybind11_tests import double_or_zero, half_or_none, test_nullopt

    if double_or_zero(None) != 0:
        raise AssertionError
    if double_or_zero(42) != 84:
        raise AssertionError
    pytest.raises(TypeError, double_or_zero, 'foo')

    if half_or_none(0) is not None:
        raise AssertionError
    if half_or_none(42) != 21:
        raise AssertionError
    pytest.raises(TypeError, half_or_none, 'foo')

    if test_nullopt() != 42:
        raise AssertionError
    if test_nullopt(None) != 42:
        raise AssertionError
    if test_nullopt(42) != 42:
        raise AssertionError
    if test_nullopt(43) != 43:
        raise AssertionError


@pytest.mark.skipif(not has_exp_optional, reason='no <experimental/optional>')
def test_exp_optional():
    from pybind11_tests import double_or_zero_exp, half_or_none_exp, test_nullopt_exp

    if double_or_zero_exp(None) != 0:
        raise AssertionError
    if double_or_zero_exp(42) != 84:
        raise AssertionError
    pytest.raises(TypeError, double_or_zero_exp, 'foo')

    if half_or_none_exp(0) is not None:
        raise AssertionError
    if half_or_none_exp(42) != 21:
        raise AssertionError
    pytest.raises(TypeError, half_or_none_exp, 'foo')

    if test_nullopt_exp() != 42:
        raise AssertionError
    if test_nullopt_exp(None) != 42:
        raise AssertionError
    if test_nullopt_exp(42) != 42:
        raise AssertionError
    if test_nullopt_exp(43) != 43:
        raise AssertionError


def test_constructors():
    """C++ default and converting constructors are equivalent to type calls in Python"""
    from pybind11_tests import (test_default_constructors, test_converting_constructors,
                                test_cast_functions)

    types = [str, bool, int, float, tuple, list, dict, set]
    expected = {t.__name__: t() for t in types}
    if test_default_constructors() != expected:
        raise AssertionError

    data = {
        str: 42,
        bool: "Not empty",
        int: "42",
        float: "+1e3",
        tuple: range(3),
        list: range(3),
        dict: [("two", 2), ("one", 1), ("three", 3)],
        set: [4, 4, 5, 6, 6, 6],
        memoryview: b'abc'
    }
    inputs = {k.__name__: v for k, v in data.items()}
    expected = {k.__name__: k(v) for k, v in data.items()}
    if test_converting_constructors(inputs) != expected:
        raise AssertionError
    if test_cast_functions(inputs) != expected:
        raise AssertionError


def test_move_out_container():
    """Properties use the `reference_internal` policy by default. If the underlying function
    returns an rvalue, the policy is automatically changed to `move` to avoid referencing
    a temporary. In case the return value is a container of user-defined types, the policy
    also needs to be applied to the elements, not just the container."""
    from pybind11_tests import MoveOutContainer

    c = MoveOutContainer()
    moved_out_list = c.move_list
    if [x.value for x in moved_out_list] != [0, 1, 2]:
        raise AssertionError


def test_implicit_casting():
    """Tests implicit casting when assigning or appending to dicts and lists."""
    from pybind11_tests import get_implicit_casting

    z = get_implicit_casting()
    if z['d'] != {
        'char*_i1': 'abc', 'char*_i2': 'abc', 'char*_e': 'abc', 'char*_p': 'abc',
        'str_i1': 'str', 'str_i2': 'str1', 'str_e': 'str2', 'str_p': 'str3',
        'int_i1': 42, 'int_i2': 42, 'int_e': 43, 'int_p': 44
    }:
        raise AssertionError
    if z['l'] != [3, 6, 9, 12, 15]:
        raise AssertionError


def test_unicode_conversion():
    """Tests unicode conversion and error reporting."""
    import pybind11_tests
    from pybind11_tests import (good_utf8_string, bad_utf8_string,
                                good_utf16_string, bad_utf16_string,
                                good_utf32_string,  # bad_utf32_string,
                                good_wchar_string,  # bad_wchar_string,
                                u8_Z, u8_eacute, u16_ibang, u32_mathbfA, wchar_heart)

    if good_utf8_string() != u"Say utf8‽ 🎂 𝐀":
        raise AssertionError
    if good_utf16_string() != u"b‽🎂𝐀z":
        raise AssertionError
    if good_utf32_string() != u"a𝐀🎂‽z":
        raise AssertionError
    if good_wchar_string() != u"a⸘𝐀z":
        raise AssertionError

    with pytest.raises(UnicodeDecodeError):
        bad_utf8_string()

    with pytest.raises(UnicodeDecodeError):
        bad_utf16_string()

    # These are provided only if they actually fail (they don't when 32-bit and under Python 2.7)
    if hasattr(pybind11_tests, "bad_utf32_string"):
        with pytest.raises(UnicodeDecodeError):
            pybind11_tests.bad_utf32_string()
    if hasattr(pybind11_tests, "bad_wchar_string"):
        with pytest.raises(UnicodeDecodeError):
            pybind11_tests.bad_wchar_string()

    if u8_Z() != 'Z':
        raise AssertionError
    if u8_eacute() != u'é':
        raise AssertionError
    if u16_ibang() != u'‽':
        raise AssertionError
    if u32_mathbfA() != u'𝐀':
        raise AssertionError
    if wchar_heart() != u'♥':
        raise AssertionError


def test_single_char_arguments():
    """Tests failures for passing invalid inputs to char-accepting functions"""
    from pybind11_tests import ord_char, ord_char16, ord_char32, ord_wchar, wchar_size

    def toobig_message(r):
        return "Character code point not in range({0:#x})".format(r)
    toolong_message = "Expected a character, but multi-character string found"

    if ord_char(u'a') != 0x61:
        raise AssertionError
    if ord_char(u'é') != 0xE9:
        raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if ord_char(u'Ā') != 0x100:
            raise AssertionError
    if str(excinfo.value) != toobig_message(0x100):
        raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if not ord_char(u'ab'):
            raise AssertionError
    if str(excinfo.value) != toolong_message:
        raise AssertionError

    if ord_char16(u'a') != 0x61:
        raise AssertionError
    if ord_char16(u'é') != 0xE9:
        raise AssertionError
    if ord_char16(u'Ā') != 0x100:
        raise AssertionError
    if ord_char16(u'‽') != 0x203d:
        raise AssertionError
    if ord_char16(u'♥') != 0x2665:
        raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if ord_char16(u'🎂') != 0x1F382:
            raise AssertionError
    if str(excinfo.value) != toobig_message(0x10000):
        raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if not ord_char16(u'aa'):
            raise AssertionError
    if str(excinfo.value) != toolong_message:
        raise AssertionError

    if ord_char32(u'a') != 0x61:
        raise AssertionError
    if ord_char32(u'é') != 0xE9:
        raise AssertionError
    if ord_char32(u'Ā') != 0x100:
        raise AssertionError
    if ord_char32(u'‽') != 0x203d:
        raise AssertionError
    if ord_char32(u'♥') != 0x2665:
        raise AssertionError
    if ord_char32(u'🎂') != 0x1F382:
        raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if not ord_char32(u'aa'):
            raise AssertionError
    if str(excinfo.value) != toolong_message:
        raise AssertionError

    if ord_wchar(u'a') != 0x61:
        raise AssertionError
    if ord_wchar(u'é') != 0xE9:
        raise AssertionError
    if ord_wchar(u'Ā') != 0x100:
        raise AssertionError
    if ord_wchar(u'‽') != 0x203d:
        raise AssertionError
    if ord_wchar(u'♥') != 0x2665:
        raise AssertionError
    if wchar_size == 2:
        with pytest.raises(ValueError) as excinfo:
            if ord_wchar(u'🎂') != 0x1F382:
                raise AssertionError
        if str(excinfo.value) != toobig_message(0x10000):
            raise AssertionError
    else:
        if ord_wchar(u'🎂') != 0x1F382:
            raise AssertionError
    with pytest.raises(ValueError) as excinfo:
        if not ord_wchar(u'aa'):
            raise AssertionError
    if str(excinfo.value) != toolong_message:
        raise AssertionError
