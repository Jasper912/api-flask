#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: Jasper Huang
# Time: 2017/11/24

from flask import request
from flask.blueprints import Blueprint as _Blueprint, BlueprintSetupState as _BlueprintSetupState
from functools import partial
from app.service.protocol import ViewFunc


class BlueprintSetupState(_BlueprintSetupState):

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if self.url_prefix:
            rule = self.url_prefix + rule

        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                              view_func(api_cls=self.blueprint.api_cls), **options)


def _pack_view_func(api_cls, func, options):
    return ViewFunc(api_cls, func, options)

class Blueprint(_Blueprint):

    api_cls = None

    def route(self, rule, **options):
        def decorator(func):
            endpoint = options.pop("endpoint", func.__name__)
            self.add_url_rule(rule,
                              endpoint,
                              partial(_pack_view_func, func=func, options=options),
                              **options)
            return func
        return decorator


    def make_setup_state(self, app, options, first_registration=False):
        # 这一层与库中源码一致，重载的目的是为了调用重载后的BlueprintSetupState
        return BlueprintSetupState(self, app, options, first_registration)
