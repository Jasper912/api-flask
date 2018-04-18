#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/11/24

from blueprints import Blueprint

class TestBlueprints(Blueprint):
    api_cls = None

test_bp = TestBlueprints("test", __name__)
