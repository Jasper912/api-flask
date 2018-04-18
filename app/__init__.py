#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/11/20

import sys
from importlib import import_module
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import request
import urlparse
from .service.protocol import CORSResponse, Request, Rule

class ActApiFlask(Flask):

    response_class = CORSResponse
    request_class = Request
    url_rule_class = Rule

    def app_init(self):
        # DB init

        self.init_api_blueprints()

    def init_api_blueprints(self):
        api_prefix_blueprint = self.config.get("API_PREFIX_BLUEPRINT")
        for api_prefix, module in api_prefix_blueprint.items():
            _, _service = self._split_module(module)

            # 引入bp 实例
            bp_name = "%s_bp" % _service
            bp_instance = self._from_import(module, bp_name)

            # 引入api
            _api_module = import_module('.api', module)

            # blueprint 注入api_cls
            cls_name = "%sApi" % _service.capitalize()
            api_path = "%s.api" % module
            api_cls = self._from_import(api_path, cls_name)
            bp_instance.api_cls = api_cls

            self.register_blueprint(bp_instance, url_prefix=api_prefix)

    def _split_module(self, module_name):
        return module_name.rsplit('.', 1)

    def _from_import(self, _from, _import):
        return getattr(import_module(_from), _import)


actapp = ActApiFlask(__name__)
actapp.config.from_pyfile("../config.py")
actapp.app_init()
