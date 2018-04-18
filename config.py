#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/09/26

"""
    项目配置相关
"""

LOG_BASE_DIR = "/data/log/test"
DB_LIST = ["test"]


# 项目api 入口控制
API_PREFIX_BLUEPRINT = {
    '/test': "app.service.test",
}
