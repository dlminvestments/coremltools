

def test_chrono_system_clock():
    from pybind11_tests import test_chrono1
    import datetime

    # Get the time from both c++ and datetime
    date1 = test_chrono1()
    date2 = datetime.datetime.today()

    # The returned value should be a datetime
    if not isinstance(date1, datetime.datetime):
        raise AssertionError

    # The numbers should vary by a very small amount (time it took to execute)
    diff = abs(date1 - date2)

    # There should never be a days/seconds difference
    if diff.days != 0:
        raise AssertionError
    if diff.seconds != 0:
        raise AssertionError

    # We test that no more than about 0.5 seconds passes here
    # This makes sure that the dates created are very close to the same
    # but if the testing system is incredibly overloaded this should still pass
    if diff.microseconds >= 500000:
        raise AssertionError


def test_chrono_system_clock_roundtrip():
    from pybind11_tests import test_chrono2
    import datetime

    date1 = datetime.datetime.today()

    # Roundtrip the time
    date2 = test_chrono2(date1)

    # The returned value should be a datetime
    if not isinstance(date2, datetime.datetime):
        raise AssertionError

    # They should be identical (no information lost on roundtrip)
    diff = abs(date1 - date2)
    if diff.days != 0:
        raise AssertionError
    if diff.seconds != 0:
        raise AssertionError
    if diff.microseconds != 0:
        raise AssertionError


def test_chrono_duration_roundtrip():
    from pybind11_tests import test_chrono3
    import datetime

    # Get the difference between two times (a timedelta)
    date1 = datetime.datetime.today()
    date2 = datetime.datetime.today()
    diff = date2 - date1

    # Make sure this is a timedelta
    if not isinstance(diff, datetime.timedelta):
        raise AssertionError

    cpp_diff = test_chrono3(diff)

    if cpp_diff.days != diff.days:
        raise AssertionError
    if cpp_diff.seconds != diff.seconds:
        raise AssertionError
    if cpp_diff.microseconds != diff.microseconds:
        raise AssertionError


def test_chrono_duration_subtraction_equivalence():
    from pybind11_tests import test_chrono4
    import datetime

    date1 = datetime.datetime.today()
    date2 = datetime.datetime.today()

    diff = date2 - date1
    cpp_diff = test_chrono4(date2, date1)

    if cpp_diff.days != diff.days:
        raise AssertionError
    if cpp_diff.seconds != diff.seconds:
        raise AssertionError
    if cpp_diff.microseconds != diff.microseconds:
        raise AssertionError


def test_chrono_steady_clock():
    from pybind11_tests import test_chrono5
    import datetime

    time1 = test_chrono5()
    time2 = test_chrono5()

    if not isinstance(time1, datetime.timedelta):
        raise AssertionError
    if not isinstance(time2, datetime.timedelta):
        raise AssertionError


def test_chrono_steady_clock_roundtrip():
    from pybind11_tests import test_chrono6
    import datetime

    time1 = datetime.timedelta(days=10, seconds=10, microseconds=100)
    time2 = test_chrono6(time1)

    if not isinstance(time2, datetime.timedelta):
        raise AssertionError

    # They should be identical (no information lost on roundtrip)
    if time1.days != time2.days:
        raise AssertionError
    if time1.seconds != time2.seconds:
        raise AssertionError
    if time1.microseconds != time2.microseconds:
        raise AssertionError


def test_floating_point_duration():
    from pybind11_tests import test_chrono7
    import datetime

    # Test using 35.525123 seconds as an example floating point number in seconds
    time = test_chrono7(35.525123)

    if not isinstance(time, datetime.timedelta):
        raise AssertionError

    if time.seconds != 35:
        raise AssertionError
    if 525122 > time.microseconds:
        raise AssertionError
