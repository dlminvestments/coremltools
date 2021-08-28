import pytest
from pybind11_tests import ConstructorStats


def test_smart_ptr(capture):
    # Object1
    from pybind11_tests import (MyObject1, make_object_1, make_object_2,
                                print_object_1, print_object_2, print_object_3, print_object_4)

    for i, o in enumerate([make_object_1(), make_object_2(), MyObject1(3)], start=1):
        if o.getRefCount() != 1:
            raise AssertionError
        with capture:
            print_object_1(o)
            print_object_2(o)
            print_object_3(o)
            print_object_4(o)
        if capture != "MyObject1[{i}]\n".format(i=i) * 4:
            raise AssertionError

    from pybind11_tests import (make_myobject1_1, make_myobject1_2,
                                print_myobject1_1, print_myobject1_2,
                                print_myobject1_3, print_myobject1_4)

    for i, o in enumerate([make_myobject1_1(), make_myobject1_2(), MyObject1(6), 7], start=4):
        print(o)
        with capture:
            if not isinstance(o, int):
                print_object_1(o)
                print_object_2(o)
                print_object_3(o)
                print_object_4(o)
            print_myobject1_1(o)
            print_myobject1_2(o)
            print_myobject1_3(o)
            print_myobject1_4(o)
        if capture != "MyObject1[{i}]\n".format(i=i) * (4 if isinstance(o, int) else 8):
            raise AssertionError

    cstats = ConstructorStats.get(MyObject1)
    if cstats.alive() != 0:
        raise AssertionError
    expected_values = ['MyObject1[{}]'.format(i) for i in range(1, 7)] + ['MyObject1[7]'] * 4
    if cstats.values() != expected_values:
        raise AssertionError
    if cstats.default_constructions != 0:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError

    # Object2
    from pybind11_tests import (MyObject2, make_myobject2_1, make_myobject2_2,
                                make_myobject3_1, make_myobject3_2,
                                print_myobject2_1, print_myobject2_2,
                                print_myobject2_3, print_myobject2_4)

    for i, o in zip([8, 6, 7], [MyObject2(8), make_myobject2_1(), make_myobject2_2()]):
        print(o)
        with capture:
            print_myobject2_1(o)
            print_myobject2_2(o)
            print_myobject2_3(o)
            print_myobject2_4(o)
        if capture != "MyObject2[{i}]\n".format(i=i) * 4:
            raise AssertionError

    cstats = ConstructorStats.get(MyObject2)
    if cstats.alive() != 1:
        raise AssertionError
    o = None
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ['MyObject2[8]', 'MyObject2[6]', 'MyObject2[7]']:
        raise AssertionError
    if cstats.default_constructions != 0:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError

    # Object3
    from pybind11_tests import (MyObject3, print_myobject3_1, print_myobject3_2,
                                print_myobject3_3, print_myobject3_4)

    for i, o in zip([9, 8, 9], [MyObject3(9), make_myobject3_1(), make_myobject3_2()]):
        print(o)
        with capture:
            print_myobject3_1(o)
            print_myobject3_2(o)
            print_myobject3_3(o)
            print_myobject3_4(o)
        if capture != "MyObject3[{i}]\n".format(i=i) * 4:
            raise AssertionError

    cstats = ConstructorStats.get(MyObject3)
    if cstats.alive() != 1:
        raise AssertionError
    o = None
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ['MyObject3[9]', 'MyObject3[8]', 'MyObject3[9]']:
        raise AssertionError
    if cstats.default_constructions != 0:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError

    # Object and ref
    from pybind11_tests import Object, cstats_ref

    cstats = ConstructorStats.get(Object)
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != []:
        raise AssertionError
    if cstats.default_constructions != 10:
        raise AssertionError
    if cstats.copy_constructions != 0:
        raise AssertionError
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    if cstats.copy_assignments != 0:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError

    cstats = cstats_ref()
    if cstats.alive() != 0:
        raise AssertionError
    if cstats.values() != ['from pointer'] * 10:
        raise AssertionError
    if cstats.default_constructions != 30:
        raise AssertionError
    if cstats.copy_constructions != 12:
        raise AssertionError
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    if cstats.copy_assignments != 30:
        raise AssertionError
    if cstats.move_assignments != 0:
        raise AssertionError


def test_smart_ptr_refcounting():
    from pybind11_tests import test_object1_refcounting
    if not test_object1_refcounting():
        raise AssertionError


def test_unique_nodelete():
    from pybind11_tests import MyObject4
    o = MyObject4(23)
    if o.value != 23:
        raise AssertionError
    cstats = ConstructorStats.get(MyObject4)
    if cstats.alive() != 1:
        raise AssertionError
    del o
    cstats = ConstructorStats.get(MyObject4)
    if cstats.alive() != 1:
        raise AssertionError


def test_shared_ptr_and_references():
    from pybind11_tests.smart_ptr import SharedPtrRef, A

    s = SharedPtrRef()
    stats = ConstructorStats.get(A)
    if stats.alive() != 2:
        raise AssertionError

    ref = s.ref  # init_holder_helper(holder_ptr=false, owned=false)
    if stats.alive() != 2:
        raise AssertionError
    if not s.set_ref(ref):
        raise AssertionError
    with pytest.raises(RuntimeError) as excinfo:
        if not s.set_holder(ref):
            raise AssertionError
    if "Unable to cast from non-held to held instance" not in str(excinfo.value):
        raise AssertionError

    copy = s.copy  # init_holder_helper(holder_ptr=false, owned=true)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(copy):
        raise AssertionError
    if not s.set_holder(copy):
        raise AssertionError

    holder_ref = s.holder_ref  # init_holder_helper(holder_ptr=true, owned=false)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(holder_ref):
        raise AssertionError
    if not s.set_holder(holder_ref):
        raise AssertionError

    holder_copy = s.holder_copy  # init_holder_helper(holder_ptr=true, owned=true)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(holder_copy):
        raise AssertionError
    if not s.set_holder(holder_copy):
        raise AssertionError

    del ref, copy, holder_ref, holder_copy, s
    if stats.alive() != 0:
        raise AssertionError


def test_shared_ptr_from_this_and_references():
    from pybind11_tests.smart_ptr import SharedFromThisRef, B

    s = SharedFromThisRef()
    stats = ConstructorStats.get(B)
    if stats.alive() != 2:
        raise AssertionError

    ref = s.ref  # init_holder_helper(holder_ptr=false, owned=false, bad_wp=false)
    if stats.alive() != 2:
        raise AssertionError
    if not s.set_ref(ref):
        raise AssertionError
    if not s.set_holder(ref):
        raise AssertionError

    bad_wp = s.bad_wp  # init_holder_helper(holder_ptr=false, owned=false, bad_wp=true)
    if stats.alive() != 2:
        raise AssertionError
    if not s.set_ref(bad_wp):
        raise AssertionError
    with pytest.raises(RuntimeError) as excinfo:
        if not s.set_holder(bad_wp):
            raise AssertionError
    if "Unable to cast from non-held to held instance" not in str(excinfo.value):
        raise AssertionError

    copy = s.copy  # init_holder_helper(holder_ptr=false, owned=true, bad_wp=false)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(copy):
        raise AssertionError
    if not s.set_holder(copy):
        raise AssertionError

    holder_ref = s.holder_ref  # init_holder_helper(holder_ptr=true, owned=false, bad_wp=false)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(holder_ref):
        raise AssertionError
    if not s.set_holder(holder_ref):
        raise AssertionError

    holder_copy = s.holder_copy  # init_holder_helper(holder_ptr=true, owned=true, bad_wp=false)
    if stats.alive() != 3:
        raise AssertionError
    if not s.set_ref(holder_copy):
        raise AssertionError
    if not s.set_holder(holder_copy):
        raise AssertionError

    del ref, bad_wp, copy, holder_ref, holder_copy, s
    if stats.alive() != 0:
        raise AssertionError


def test_move_only_holder():
    from pybind11_tests.smart_ptr import TypeWithMoveOnlyHolder

    a = TypeWithMoveOnlyHolder.make()
    stats = ConstructorStats.get(TypeWithMoveOnlyHolder)
    if stats.alive() != 1:
        raise AssertionError
    del a
    if stats.alive() != 0:
        raise AssertionError
