from lava_test_plans.__main__ import main

from unittest import TestCase
import sys
import glob
import os
import pytest
import shlex

test_lava_validity = (
    "" if os.getenv("SKIP_TEST_LAVA_VALIDITY") else "--test-lava-validity"
)

devices = ["hi960-hikey", "x15", "qemu_arm64"]
testcase = "ltp-syscalls.yaml"
variable_input_files = ["test/variables-tags.ini", "test/variables-tags-one-tag.ini"]
tests = []
for device in devices:
    for variable_file in variable_input_files:
        tests.append((variable_file, device, testcase))


@pytest.mark.parametrize("param", tests)
def test_call_lava_tags_testcase(param):
    variable_input_file, device, testcase = param
    sys.argv = shlex.split(
        f'lava_test_plans --dry-run --variables "{variable_input_file}" --device-type "{device}" --test-case "{testcase}" {test_lava_validity}'
    )
    assert main() == 0
