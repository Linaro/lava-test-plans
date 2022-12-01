from lava_test_plans.__main__ import main

from unittest import TestCase
import sys
import glob
import os
import pytest


devices = ['hi960-hikey', 'x15', 'qemu_arm64']
testcase = 'ltp-syscalls.yaml'
variable_input_file = "test/variables-visibility.ini"
tests = []
for device in devices:
    tests.append((variable_input_file, device, testcase))


@pytest.mark.parametrize("param", tests)
def test_call_lava_visibility_group_testcase(param):
    variable_input_file, device, testcase = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-case", testcase, "--test-lava-validity"]
    assert main() == 0
