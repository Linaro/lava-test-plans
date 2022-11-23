from lava_test_plans.__main__ import main

from unittest import TestCase
import sys
import glob
import os
from multiprocessing import Pool


def call_lava_test_plan_testcases(param):
    variable_input_file, device, testcase = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-case", testcase]
    return main() == 0


def call_lava_test_plan_testplans(param):
    variable_input_file, device, testplan = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    return main() == 0


def call_lava_test_plan_testcases_project(param):
    variable_input_file, device, testcase, project_device_path = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--testplan-device-path", project_device_path, "--device-type", device, "--test-case", testcase, "--test-lava-validity"]
    return main() == 0


def call_lava_test_plan_testplans_project(param):
    variable_input_file, device, testplan, project_device_path = param
    sys.argv = ["lava_test_plans", "--dry-run", "--variables", variable_input_file, "--testplan-device-path", project_device_path, "--device-type", device, "--test-plan", testplan, "--test-lava-validity"]
    return main() == 0


class TestLavaTestPlans(TestCase):

    def test_testcases_without_project(self):
        devices = [os.path.basename(d) for d in glob.glob("lava_test_plans/devices/*")]
        testcases = [os.path.basename(d) for d in glob.glob("lava_test_plans/testcases/*.yaml")]
        variable_input_file = "variables.ini"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testcase) for testcase in testcases]
                results = p.map(call_lava_test_plan_testcases, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testplan_with_project_armnn(self):
        devices = [os.path.basename(d) for d in glob.glob("projects/armnn/devices")]
        testplans = ['armnn', 'armnn-benchmarking']
        variable_input_file = "projects/armnn/variables.yaml"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testplan) for testplan in testplans]
                results = p.map(call_lava_test_plan_testplans, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testcases_with_project_lkft(self):
        project_device_path = "lava_test_plans/projects/lkft/devices"
        devices = [os.path.basename(d) for d in glob.glob("projects/lkft/devices")]
        testcases = [os.path.basename(d) for d in glob.glob("lava_test_plans/testcases/*.yaml")]
        variable_input_file = "projects/lkft/variables.ini"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testcase, project_device_path) for testcase in testcases]
                results = p.map(call_lava_test_plan_testcases_project, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testplan_with_project_lkft(self):
        project_device_path = "lava_test_plans/projects/lkft/devices"
        devices = [os.path.basename(d) for d in glob.glob("projects//devices")]
        testplans = ['lkft-full', 'lkft-kselftest', 'lkft-ltp', 'lkft-rt', 'lkft-sanity']
        variable_input_file = "projects/lkft/variables.ini"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testplan, project_device_path) for testplan in testplans]
                results = p.map(call_lava_test_plan_testplans_project, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testplan_with_project_lt_qcom(self):
        project_device_path = "lava_test_plans/projects/lt-qcom/devices"
        devices = [os.path.basename(d) for d in glob.glob("projects/lt-qcom/devices")]
        testplans = ['lt-qcom/distro', 'lt-qcom/kernel']
        variable_input_file = "projects/lt-qcom/variables.ini"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testplan, project_device_path) for testplan in testplans]
                results = p.map(call_lava_test_plan_testplans_project, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testplan_with_project_tf_a(self):
        project_device_path = "lava_test_plans/projects/tf-a/devices"
        devices = [os.path.basename(d) for d in glob.glob("projects/tf-a/devices")]
        testplans = ['tf-a']
        variable_input_file = "projects/tf-a/variables.yaml"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testplan, project_device_path) for testplan in testplans]
                results = p.map(call_lava_test_plan_testplans_project, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)

    def test_testplan_with_project_ti(self):
        devices = [os.path.basename(d) for d in glob.glob("projects/ti/devices")]
        testplans = ['ti-uboot']
        variable_input_file = "projects/ti/variables.yaml"
        with Pool() as p:
            for device in devices:
                tests = [(variable_input_file, device, testplan) for testplan in testplans]
                results = p.map(call_lava_test_plan_testplans, tests)
                self.assertTrue(all(results))
        self.assertTrue(True)
