import os


def test_evals(capture):
    from pybind11_tests import (test_eval_statements, test_eval, test_eval_single_statement,
                                test_eval_file, test_eval_failure, test_eval_file_failure)

    with capture:
        if not test_eval_statements():
            raise AssertionError
    if capture != "Hello World!":
        raise AssertionError

    if not test_eval():
        raise AssertionError
    if not test_eval_single_statement():
        raise AssertionError

    filename = os.path.join(os.path.dirname(__file__), "test_eval_call.py")
    if not test_eval_file(filename):
        raise AssertionError

    if not test_eval_failure():
        raise AssertionError
    if not test_eval_file_failure():
        raise AssertionError
