from lava_test_plans.__main__ import main

from unittest import TestCase
import sys
import glob
import os
import pytest


# all tests all devices
devices = [os.path.basename(d) for d in glob.glob("lava_test_plans/devices/*")]
testcases = [os.path.basename(d) for d in glob.glob("lava_test_plans/testcases/*.yaml")]
variable_input_file = "variables.ini"
tests = []
for device in devices:
    for testcase in testcases:
        tests.append((variable_input_file, device, testcase))


@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testcases(param):
    variable_input_file, device, testcase = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-case", testcase]
    assert main() == 0


# armnn tests
armnn_devices = ['hi960-hikey', 'dragonboard-845c', 'synquacer', 'stm32mp157c-dk2', 'juno']
assert len(armnn_devices) > 0
armnn_testplans = ['armnn', 'armnn-benchmarking']
assert len(armnn_testplans) > 0
armnn_variable_input_file = "projects/armnn/variables.yaml"
tests = []
for device in armnn_devices:
    for testplan in armnn_testplans:
        tests.append((armnn_variable_input_file, device, testplan))


@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testplans_armnn(param):
    variable_input_file, device, testplan = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    assert main() == 0


# lkft tests
lkft_project_device_path = "lava_test_plans/projects/lkft/devices"
lkft_devices = [os.path.basename(d) for d in glob.glob("lava_test_plans/projects/lkft/devices/*")]
assert len(lkft_devices) > 0
lkft_testplans = ['lkft-full', 'lkft-kselftest', 'lkft-ltp', 'lkft-rt', 'lkft-sanity']
assert len(lkft_testplans) > 0
lkft_variable_input_file = "projects/lkft/variables.ini"
tests = []
for device in lkft_devices:
    for testplan in lkft_testplans:
        tests.append((lkft_variable_input_file, device, testplan, lkft_project_device_path))


@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testplans_project_lkft(param):
    variable_input_file, device, testplan, project_device_path = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--testplan-device-path", project_device_path, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    assert main() == 0


# lt-qcom tests
lt_qcom_project_device_path = "lava_test_plans/projects/lt-qcom/devices"
lt_qcom_devices = [os.path.basename(d) for d in glob.glob("lava_test_plans/projects/lt-qcom/devices/*")]
assert len(lt_qcom_devices) > 0
lt_qcom_testplans = ['lt-qcom/kernel']
assert len(lt_qcom_testplans) > 0
lt_qcom_variable_input_file = "projects/lt-qcom/variables.yaml"
tests = []
for device in lt_qcom_devices:
    for testplan in lt_qcom_testplans:
        tests.append((lt_qcom_variable_input_file, device, testplan, lt_qcom_project_device_path))

@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testplans_project_lt_qcom(param):
    variable_input_file, device, testplan, project_device_path = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--testplan-device-path", project_device_path, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    assert main() == 0


# tf-a tests
tf_a_project_device_path = "lava_test_plans/projects/tf-a/devices"
tf_a_devices = [os.path.basename(d) for d in glob.glob("lava_test_plans/projects/tf-a/devices/*")]
assert len(tf_a_devices) > 0
tf_a_testplans = ['tf-a']
assert len(tf_a_testplans) > 0
tf_a_variable_input_file = "projects/tf-a/variables.yaml"
tests = []
for device in tf_a_devices:
    for testplan in tf_a_testplans:
        tests.append((tf_a_variable_input_file, device, testplan, tf_a_project_device_path))


@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testplans_project_tf_a(param):
    variable_input_file, device, testplan, project_device_path = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--testplan-device-path", project_device_path, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    assert main() == 0


# ti tests
ti_devices = ['x15-bl']
assert len(ti_devices) > 0
ti_testplans = ['ti-uboot']
assert len(ti_testplans) > 0
ti_variable_input_file = "projects/ti/variables.yaml"
tests = []
for device in ti_devices:
    for testplan in ti_testplans:
        tests.append((ti_variable_input_file, device, testplan))


@pytest.mark.parametrize("param", tests)
def test_call_lava_test_plan_testplans_ti(param):
    variable_input_file, device, testplan = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    assert main() == 0, f"fail: {sys.argv}"
