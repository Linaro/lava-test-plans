#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
from configobj import ConfigObj, ConfigObjError
import fnmatch
from io import StringIO
import itertools
import logging
import os
import re
import requests
import sys

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    make_logging_undefined,
)
from jinja2.exceptions import UndefinedError, TemplateSyntaxError
from ruamel.yaml import YAML
from ruamel.yaml.constructor import (
    DuplicateKeyError,
    ConstructorError,
    DuplicateKeyFutureWarning,
)
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.parser import ParserError
from ruamel.yaml.composer import ComposerError

from lava_test_plans import __version__


FORMAT = "[%(funcName)16s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit


# Templates base path
script_dirname = os.path.dirname(os.path.abspath(__file__))
template_base_path = script_dirname
testplan_base_path = os.path.join(script_dirname, "testplans/")
testcase_base_path = os.path.join(script_dirname, "testcases/")
testplan_device_path = os.path.join(script_dirname, "devices/")


def parse_template(yaml_string):
    """
    Round trip lava_job through ruamel to test parsing and
    improve formatting. Comments are preserved.

    In: yaml-formatted string
    Out: validated yaml-formatted string
    """
    logger.debug(yaml_string)
    yaml = YAML()
    # ruamel does not provide a mechanism to dump to string, so use StringIO
    # to catch it
    output = StringIO()
    yaml.dump(yaml.load(yaml_string), output)
    # strip empty lines from output
    return re.sub(r"^\s*$\n", "", output.getvalue(), flags=re.MULTILINE)


def get_job_name(lava_job_string):
    """
    In: yaml-formatted string
    Out: LAVA job's name
    """
    yaml = YAML()
    lava_job = yaml.load(lava_job_string)
    return lava_job["job_name"]


def _load_template(template_name, template_path, device_type):
    template = ""
    template_file_name = ""

    if template_name:
        template_file_name = "%s/%s/%s" % (template_path, device_type, template_name)
        if os.path.exists(template_file_name):
            with open(template_file_name, "r") as f:
                template = f.read()
        else:
            logger.error(
                "template (%s) was specified but does not exist" % template_file_name
            )
            return 1

    return template, template_file_name


def _get_test_plan_list(test_plan_path):
    """
    Returns list of all .yaml files in the directory
    specified as parameter
    """
    logger.debug("Checking for files in %s" % test_plan_path)
    ret_list = []
    for filename in os.listdir(test_plan_path):
        if fnmatch.fnmatch(filename, "*.yaml"):
            ret_list.append(filename)
    logger.debug(ret_list)
    return ret_list


def _submit_to_squad(lava_job, lava_url_base, qa_server_api, qa_server_base, qa_token):
    headers = {"Auth-Token": qa_token}

    try:
        data = {
            "definition": lava_job,
            "backend": urlsplit(
                lava_url_base
            ).netloc,  # qa-reports backends are named as lava instances
        }
        logger.info("Submit to: %s" % qa_server_api)
        response = requests.post(qa_server_api, data=data, headers=headers, timeout=31)

        logger.info(
            "%s/testjob/%s %s" % (qa_server_base, response.text, get_job_name(lava_job))
        )
        logger.info(response.status_code)
        logger.info(response.text)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error("QA Reports submission failed")
        logger.info("offending job definition:")
        logger.info(lava_job)
        return 1


def _submit_to_lava(lava_job, lava_url_base, lava_username, lava_token):
    pass


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s, {__version__}"
    )

    # qa-reports parameters
    parser.add_argument(
        "--environment",
        help="User specified the environment name, prefix or suffix won't be used",
        dest="environment",
        default="",
    )
    parser.add_argument(
        "--env-prefix",
        help="Prefix for the environment name",
        dest="env_prefix",
        default="",
    )
    parser.add_argument(
        "--env-suffix",
        help="Suffix for the environment name",
        dest="env_suffix",
        default="",
    )
    parser.add_argument(
        "--build-id", "--build-number", help="ID for the build", dest="build_id"
    )
    parser.add_argument(
        "--qa-server-team", help="Team in QA Reports service", dest="qa_server_team"
    )
    parser.add_argument(
        "--qa-server-project",
        help="Project in QA Reports service",
        dest="qa_server_project",
    )
    parser.add_argument(
        "--qa-server",
        help="QA Reports server",
        dest="qa_server",
        default="https://qa-reports.linaro.org",
    )
    parser.add_argument(
        "--qa-token",
        help="QA Reports token",
        dest="qa_token",
        default=os.environ.get("QA_REPORTS_TOKEN"),
    )
    # lava parameters
    parser.add_argument("--lava-server", help="LAVA server URL", dest="lava_server")
    parser.add_argument("--lava-username", help="LAVA username", dest="lava_username")
    parser.add_argument(
        "--lava-token", help="LAVA authentication token", dest="lava_token"
    )
    # rendering parameters (test plan)
    parser.add_argument(
        "--variables",
        help="Path to file(s) with variable values",
        dest="variables",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "--overwrite-variables",
        help="Key-value pairs overwriting variables from the file",
        nargs="+",
        dest="overwrite_variables",
        default=[],
    )
    parser.add_argument(
        "--device-type", help="Device type in LAVA", dest="device_type", required=True
    )
    parser.add_argument(
        "--template-path",
        help="Path to LAVA job templates",
        dest="template_path",
        default=template_base_path,
    )
    parser.add_argument(
        "--testplan-path",
        help="Path to directory containing all test plans",
        dest="testplan_path",
        default=testplan_base_path,
    )
    parser.add_argument(
        "--testcase-path",
        help="Path to directory containing all test cases",
        dest="testcase_path",
        default=testcase_base_path,
    )
    parser.add_argument(
        "--testplan-device-path",
        help="Relative path to Jinja2 device deployment fragments",
        dest="testplan_device_path",
        default=testplan_device_path,
    )
    parser.add_argument(
        "--test-plan",
        help="""Directories containing Jinja2 templates to submit for testing.
                        It is assumed that the templates produce valid LAVA job
                        definitions. All variables are substituted using Jinja2
                        engine""",
        dest="test_plan",
        nargs="*",
        required=False,
    )
    parser.add_argument(
        "--test-case",
        help="""Specific test cases (as Jinja2 templates) to submit.
                        It is assumed that the templates produce valid LAVA job
                        definitions. All variables are substituted using Jinja2
                        engine. Multiple --test-case variables are allowed:
                        --test-case test1.yaml test2.yaml --test-case test3.yaml""",
        dest="test_case",
        nargs="*",
        action="append",
        required=False,
    )
    parser.add_argument(
        "--dry-run",
        help="""Prepare and write templates to tmp/.
                        Don't submit to actual servers.""",
        action="store_true",
        dest="dryrun",
    )
    parser.add_argument(
        "--test-lava-validity",
        help="""Test generated templates using LAVA container validator""",
        action="store_true",
        dest="test_lava_validity",
    )
    parser.add_argument(
        "--verbose",
        help="""Verbosity level. Follows logging levels:
                          CRITICAL: 50
                          ERROR: 40
                          WARNING: 30
                          INFO: 20
                          DEBUG: 10
                          NOTSET: 0""",
        dest="verbose",
        type=int,
        default=logging.INFO,
    )

    args = parser.parse_args()
    logger.setLevel(args.verbose)
    exit_code = 0

    output_path = os.path.abspath(os.path.join(script_dirname, "..", "tmp"))

    if not os.path.isabs(args.testplan_path):
        if not os.path.isdir(args.testplan_path):
            args.testplan_path = os.path.join(script_dirname, args.testplan_path)
    if not os.path.isabs(args.testcase_path):
        if not os.path.isdir(args.testcase_path):
            args.testcase_path = os.path.join(script_dirname, args.testcase_path)
    if not os.path.isabs(args.testplan_device_path):
        if not os.path.isdir(args.testplan_device_path):
            args.testplan_device_path = os.path.join(
                script_dirname, args.testplan_device_path
            )

    if args.qa_server_project:
        if "/" in args.qa_server_project:
            logger.error("--qa-server-project can not contain of a slash in the name")
            return 1

    if args.dryrun:
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
    if args.qa_token is None and args.lava_token is None and not args.dryrun:
        logger.error("QA_REPORTS_TOKEN and LAVA_TOKEN are missing")
        return 1

    lava_jobs = []

    template_dirs = [
        os.path.abspath(template_base_path),
        os.path.abspath(args.testplan_path),
        os.path.abspath(args.testcase_path),
        os.path.abspath(args.testplan_device_path),
    ]
    # prevent creating templates when variables are missing
    j2_env = Environment(
        loader=FileSystemLoader(template_dirs, followlinks=True),
        undefined=make_logging_undefined(logger=logger, base=StrictUndefined)
        if args.dryrun
        else StrictUndefined,
    )
    context = {}
    for variables in args.variables:
        if not os.path.exists(variables):
            variables = os.path.join(script_dirname, variables)
        try:
            context.update(ConfigObj(variables).dict())
        except ConfigObjError:
            logger.info("Unable to parse .ini file")
            logger.info("Trying YAML")
            with open(variables, "r") as vars_file:
                try:
                    yaml = YAML(typ="safe")
                    context.update(yaml.load(vars_file))
                except ParserError as e:
                    logger.error(e)
                except ComposerError as e:
                    logger.error(e)

    for variable in args.overwrite_variables:
        key, value = variable.split("=")
        context.update({key: value})
    context.update({"device_type": args.device_type})
    test_list = []
    if args.test_plan:
        for test_plan in args.test_plan:
            test_plan_path = os.path.abspath(
                os.path.join(args.testplan_path, test_plan)
            )
            for test in _get_test_plan_list(test_plan_path):
                test_list.append(test)

    if args.test_case:
        test_list = test_list + list(itertools.chain.from_iterable(args.test_case))

    if len(test_list) == 0:
        logger.error("No tests matched the given criteria.")
        return 1

    # convert test_list to set to remove potential duplicates
    for test in set(test_list):
        """Prepare lava jobs"""
        lava_job = None
        try:
            lava_job = j2_env.get_template(test).render(context)
            lava_job = parse_template(lava_job)
            lava_jobs.append(lava_job)

            logger.debug(lava_job)
        except DuplicateKeyError as e:
            logger.error(e)
            exit_code = 1
        except ConstructorError as e:
            logger.error(e)
            exit_code = 1
        except DuplicateKeyFutureWarning as e:
            logger.error(e)
            exit_code = 1
        except ScannerError as e:
            logger.error(e)
            exit_code = 1
        except ParserError as e:
            testpath = os.path.join(output_path, args.device_type, test)
            logger.error("Failed to parse: %s" % testpath)
            logger.error(e)
            exit_code = 1
        except TemplateSyntaxError as e:
            testpath = os.path.join(output_path, args.device_type, test)
            logger.error("Trying to render: %s" % testpath)
            logger.error("Error in file: %s" % e.name)
            logger.error("\tline: %s" % e.lineno)
            logger.error("\tissue: %s" % e.message)
            exit_code = 1
        except UndefinedError as e:
            testpath = os.path.join(output_path, args.device_type, test)
            logger.error("Trying to render: %s" % testpath)
            logger.error("\tissue: %s" % e.message)
            exit_code = 1
        if args.dryrun and lava_job is not None:
            testpath = os.path.join(
                output_path, args.device_type, os.path.basename(test)
            )
            logger.info(testpath)
            if not os.path.exists(os.path.dirname(testpath)):
                os.makedirs(os.path.dirname(testpath), exist_ok=True)
            with open(os.path.join(testpath), "w") as f:
                f.write(lava_job)

    if args.test_lava_validity:
        import docker

        client = docker.from_env(version="1.38")
        logger.debug("Checking for LAVA validity")
        for test in set(test_list):
            testpath = os.path.join(os.getcwd(), output_path, args.device_type)
            logger.debug(testpath)
            logger.debug(test)
            container = client.containers.run(
                image="lavasoftware/lava-server:latest",
                command="/usr/share/lava-common/lava-schema.py job /data/%s" % test,
                volumes={"%s" % testpath: {"bind": "/data", "mode": "rw"}},
                detach=True,
            )
            container_exit_code = container.wait()
            logger.debug(exit_code)
            if container_exit_code["StatusCode"] != 0:
                logger.error("LAVA validation of %s/%s failed" % (testpath, test))
                logger.error(container.logs())
                exit_code = 1

    if not args.dryrun:
        if not args.qa_server:
            logger.error("QA-reports server not specified")
            exit_code = 1
        if not args.lava_server:
            logger.error("Lava server not specified")
            exit_code = 1

        if exit_code != 0:
            return exit_code

        qa_server_base = args.qa_server
        if not (
            qa_server_base.startswith("http://")
            or qa_server_base.startswith("https://")
        ):
            qa_server_base = "https://" + qa_server_base
        qa_server_team = args.qa_server_team
        qa_server_project = args.qa_server_project
        qa_server_build = args.build_id

        if not args.environment:
            # when user not specify value for the environment option,
            # use the device_type as before
            qa_server_env = args.env_prefix + args.device_type + args.env_suffix
        else:
            # when user specified value for the environment option,
            # use the user specified value
            qa_server_env = args.environment

        qa_server_api = "%s/api/submitjob/%s/%s/%s/%s" % (
            qa_server_base,
            qa_server_team,
            qa_server_project,
            qa_server_build,
            qa_server_env,
        )
        lava_server = args.lava_server
        if not (
            lava_server.startswith("http://") or lava_server.startswith("https://")
        ):
            lava_server = "https://" + lava_server
        lava_url_base = "%s://%s/" % (
            urlsplit(lava_server).scheme,
            urlsplit(lava_server).netloc,
        )

        for lava_job in lava_jobs:
            """Submit lava jobs"""
            if args.qa_token:
                _submit_to_squad(
                    lava_job,
                    lava_url_base,
                    qa_server_api,
                    qa_server_base,
                    args.qa_token,
                )
            if args.lava_token:
                _submit_to_lava(
                    lava_job, lava_url_base, args.lava_username, args.lava_token
                )
    else:
        return exit_code


if __name__ == "__main__":
    sys.exit(main())
