#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

"""
Generate LAVA job definitions for different devices and tests
"""

__version__ = "3.2.0"

from functools import lru_cache
from pathlib import Path

import jinja2


BASE = Path(__file__).parent.resolve()


@lru_cache(maxsize=None)
def env():
    return jinja2.Environment(
        autoescape=False,
        loader=jinja2.FileSystemLoader(
            [BASE, BASE / "testplans", BASE / "testcases", BASE / "devices"],
            followlinks=True,
        ),
        # undefined=jinja2.StrictUndefined,
    )


def render(template, context):
    data = env().get_template(template).render(**context)
    return "\n".join(l for l in data.split("\n") if l)
