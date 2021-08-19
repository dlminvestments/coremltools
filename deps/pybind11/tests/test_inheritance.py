import pytest


def test_inheritance(msg):
    from pybind11_tests import Pet, Dog, Rabbit, Hamster, dog_bark, pet_name_species

    roger = Rabbit('Rabbit')
    if roger.name() + " is a " + roger.species() != "Rabbit is a parrot":
        raise AssertionError
    if pet_name_species(roger) != "Rabbit is a parrot":
        raise AssertionError

    polly = Pet('Polly', 'parrot')
    if polly.name() + " is a " + polly.species() != "Polly is a parrot":
        raise AssertionError
    if pet_name_species(polly) != "Polly is a parrot":
        raise AssertionError

    molly = Dog('Molly')
    if molly.name() + " is a " + molly.species() != "Molly is a dog":
        raise AssertionError
    if pet_name_species(molly) != "Molly is a dog":
        raise AssertionError

    fred = Hamster('Fred')
    if fred.name() + " is a " + fred.species() != "Fred is a rodent":
        raise AssertionError

    if dog_bark(molly) != "Woof!":
        raise AssertionError

    with pytest.raises(TypeError) as excinfo:
        dog_bark(polly)
    if msg(excinfo.value) != """
        dog_bark(): incompatible function arguments. The following argument types are supported:
            1. (arg0: m.Dog) -> str

        Invoked with: <m.Pet object at 0>
    """:
        raise AssertionError


def test_automatic_upcasting():
    from pybind11_tests import return_class_1, return_class_2, return_class_n, return_none

    if type(return_class_1()).__name__ != "DerivedClass1":
        raise AssertionError
    if type(return_class_2()).__name__ != "DerivedClass2":
        raise AssertionError
    if type(return_none()).__name__ != "NoneType":
        raise AssertionError
    # Repeat these a few times in a random order to ensure no invalid caching
    # is applied
    if type(return_class_n(1)).__name__ != "DerivedClass1":
        raise AssertionError
    if type(return_class_n(2)).__name__ != "DerivedClass2":
        raise AssertionError
    if type(return_class_n(0)).__name__ != "BaseClass":
        raise AssertionError
    if type(return_class_n(2)).__name__ != "DerivedClass2":
        raise AssertionError
    if type(return_class_n(2)).__name__ != "DerivedClass2":
        raise AssertionError
    if type(return_class_n(0)).__name__ != "BaseClass":
        raise AssertionError
    if type(return_class_n(1)).__name__ != "DerivedClass1":
        raise AssertionError


def test_isinstance():
    from pybind11_tests import test_isinstance, Pet, Dog

    objects = [tuple(), dict(), Pet("Polly", "parrot")] + [Dog("Molly")] * 4
    expected = (True, True, True, True, True, False, False)
    if test_isinstance(objects) != expected:
        raise AssertionError


def test_holder():
    from pybind11_tests import test_mismatched_holder_type_1, test_mismatched_holder_type_2

    with pytest.raises(RuntimeError) as excinfo:
        test_mismatched_holder_type_1()

    if str(excinfo.value) != ("generic_type: type \"MismatchDerived1\" does not have "
                                  "a non-default holder type while its base "
                                  "\"MismatchBase1\" does"):
        raise AssertionError

    with pytest.raises(RuntimeError) as excinfo:
        test_mismatched_holder_type_2()

    if str(excinfo.value) != ("generic_type: type \"MismatchDerived2\" has a "
                                  "non-default holder type while its base "
                                  "\"MismatchBase2\" does not"):
        raise AssertionError
