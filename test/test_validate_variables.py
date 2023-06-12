from lava_test_plans.__main__ import main

import sys
import shlex


def test_validate_variables_happy_flow():
    sys.argv = shlex.split(
        f'lava_test_plans --variables "test/variables-valid.ini" --device-type "x15" --testplan-device-path "projects/lkft/devices" --validate-variables --overwrite-variables "KERNEL_BRANCH=master"'
    )
    assert main() == 0


def test_validate_variables_failure():
    sys.argv = shlex.split(
        f'lava_test_plans --variables "test/variables-invalid.yaml" --device-type "x15" --testplan-device-path "projects/lkft/devices" --validate-variables'
    )
    assert main() == 1
