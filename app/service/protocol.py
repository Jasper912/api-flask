#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/11/22
import ujson as json
from app.errcode import ErrorCode
from flask import Response as FlaskResponse
from flask import Request as FlaskRequest
from werkzeug.datastructures import Headers
import urlparse
from flask import request
from werkzeug.routing import Rule as _Rule
from app.errcode import actcode, ErrorCode
from datetime import datetime

class Rule(_Rule):

    def __init__(self, string, defaults=None, subdomain=None, methods=None,
                 build_only=False, endpoint=None, strict_slashes=None,
                 redirect_to=None, alias=False, host=None, **options):
        super(Rule, self).__init__(string, defaults, subdomain, methods,
                                   build_only, endpoint, strict_slashes,
                                   redirect_to, alias, host)


class CORSResponse(FlaskResponse):

    def __init__(self, response, **kwargs):
        _headers = kwargs.get("headers")
        _add_headers = [
            ('Content-type', 'application/json; charset=UTF-8'),
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT"),
        ]
        if isinstance(_headers, Headers):
            _headers.extends(_add_headers)
        else:
            _headers = Headers(_add_headers)

        kwargs['headers'] = _headers
        super(CORSResponse, self).__init__(response, **kwargs)


class Request(FlaskRequest):

    def get_args(self):
        args = dict(self.args)
        _post_args = self.get_post_data()
        args.update(_post_args)
        return args

    def get_post_data(self):
        qs = self.get_data()
        return dict(urlparse.parse_qsl(qs))


class Response(dict):

    def __init__(self, data):
        self.items = {
            "c": 0,
        }
        if isinstance(data, (dict, list)):
            self.items['d'] = data

        super(Response, self).__init__(self.items)


class ErrorResponse(dict):

    def __init__(self, error):
        assert isinstance(error, ErrorCode)
        self.data = {
            "c": error.code,
            "err": error.msg,
        }
        super(ErrorResponse, self).__init__(self.data)


class ApiBase(object):

    def __init__(self):
        self.args = self.get_query_args()
        self.error = None
        self.public_params = self._init_public_params()
        self.uid = None

    def _init_public_params(self):
        public_params = {
            "ip": request.remote_addr,
        }
        return public_params

    def get_query_args(self):
        return request.get_args()

    def return_success(self, rep=True):
        return json.dumps(Response(rep))

    def return_error(self):
        err_code = ErrorCode(*self.error)
        return json.dumps(ErrorResponse(err_code))

    def check_login(self):
        token = self.args.get("token", None)
        if not token:
            self.error = actcode.WEB_TOKEN_NOT_FOUND
            return False

        return True


class ViewFunc(object):

    def __init__(self, api_cls, func, options):
        self.api_cls = api_cls
        self.func = func
        self.options = options

    def __call__(self, *args, **kwargs):
        """ dispatch_request 调用方式：
            return self.view_functions[rule.endpoint](**req.view_args)
        """
        _service  = self.api_cls()
        if self.options.get("login_required"):
            if not _service.check_login():
                return self.make_up_response(_service, False)

        res = self.func(_service)
        return self.make_up_response(_service, res)

    def make_up_response(self, _service, res):
        if not res:
            return _service.return_error()
        else:
            return _service.return_success(res)

