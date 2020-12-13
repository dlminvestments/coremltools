import sys
import test_cmake_build

if test_cmake_build.add(1, 2) != 3:
    raise AssertionError
print("{} imports, runs, and adds: 1 + 2 = 3".format(sys.argv[1]))
