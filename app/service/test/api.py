#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/11/24

from . import test_bp

from app.service.protocol import ApiBase

class TestApi(ApiBase):

    @test_bp.route("/get", methods=['GET'], login_required=False)
    def get_name(self):
        res = {
            "name": "Test"
        }

        return res
