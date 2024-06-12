#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2023-present Linaro Limited
#
# SPDX-License-Identifier: MIT


import os
import argparse
import logging
from configobj import ConfigObj, ConfigObjError
from ruamel.yaml import YAML


FORMAT = "[%(funcName)16s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def get_context(script_dirname, args_variables, args_overwrite_variables):
    context = {}
    for variables in args_variables:
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

    for variable in args_overwrite_variables:
        key, value = variable.split("=")
        context.update({key: value})
    return context


def validate_variables(
    script_dirname, device_type, device_path, variables, overwrite_variables
):
    context = set(get_context(script_dirname, variables, overwrite_variables).keys())
    ref_vars = os.path.join(
        os.path.abspath(os.path.join(script_dirname, device_path)),
        "variables",
        f"{device_type}.yaml",
    )
    ref_variables = set()
    with open(ref_vars, "r") as vars_file:
        yaml = YAML(typ="safe")
        ref_variables = set(yaml.load(vars_file).keys())
    var_diff = ref_variables.difference(context)
    if var_diff:
        logger.error(f"Mandatory variables missing: {var_diff}")
        return 1
    return 0


class overlay_action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        entries = len(values)

        pairs = getattr(namespace, self.dest, [])

        if entries > 2:
            parser.error(
                f"More than 2 arguments passed for {self.dest} options. Please check help options"
            )

        if entries == 1:
            pairs.append([values[0], "/"])
        else:
            pairs.append([values[0], values[1]])
        setattr(namespace, self.dest, pairs)


COMPRESSIONS = {
    ".tar.xz": ("tar", "xz"),
    ".tar.gz": ("tar", "gz"),
    ".tgz": ("tar", "gz"),
    ".gz": (None, "gz"),
    ".xz": (None, "xz"),
    ".zst": (None, "zstd"),
    ".py": ("file", None),
    ".sh": ("file", None),
}


def compression(path):
    for ext, ret in COMPRESSIONS.items():
        if path.endswith(ext):
            return ret
    return (None, None)
