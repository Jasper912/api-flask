## 前言
* flask 框架route 是注册在普通函数上，开发中沿用一些公共函数不是很方便。通过重写blueprint.route ，api 注册在类方法上，沿用
 类的一些公共方法，统一交互协议。


## 思路
* 请求入口， Flask.app.wsgi_app
* flask 路由执行的一句关键代码在于 flask.app.dispatch_request 下的 `self.view_functions[rule.endpoint](**req.view_args)`, view_functions是app的路由map, 根据endpoint 找到对应的view_function
* Flask.app.register_blueprint 中可以将一个blueprint 对象注册进app，尝试通过改写 blueprint.route 实现该功能
* 自定义ViewFunction，实现 `__call__` 方法满足dispatch_request 的调用

