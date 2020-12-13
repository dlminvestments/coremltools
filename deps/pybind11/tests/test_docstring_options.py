

def test_docstring_options():
    from pybind11_tests import (test_function1, test_function2, test_function3,
                                test_function4, test_function5, test_function6,
                                test_function7, DocstringTestFoo)

    # options.disable_function_signatures()
    if test_function1.__doc__:
        raise AssertionError

    if test_function2.__doc__ != "A custom docstring":
        raise AssertionError

    # options.enable_function_signatures()
    if not test_function3.__doc__ .startswith("test_function3(a: int, b: int) -> None"):
        raise AssertionError

    if not test_function4.__doc__ .startswith("test_function4(a: int, b: int) -> None"):
        raise AssertionError
    if not test_function4.__doc__ .endswith("A custom docstring\n"):
        raise AssertionError

    # options.disable_function_signatures()
    # options.disable_user_defined_docstrings()
    if test_function5.__doc__:
        raise AssertionError

    # nested options.enable_user_defined_docstrings()
    if test_function6.__doc__ != "A custom docstring":
        raise AssertionError

    # RAII destructor
    if not test_function7.__doc__ .startswith("test_function7(a: int, b: int) -> None"):
        raise AssertionError
    if not test_function7.__doc__ .endswith("A custom docstring\n"):
        raise AssertionError

    # Suppression of user-defined docstrings for non-function objects
    if DocstringTestFoo.__doc__:
        raise AssertionError
    if DocstringTestFoo.value_prop.__doc__:
        raise AssertionError
