# coding=utf-8

import json
from enum import Enum
from typing import Callable, Any
from flask import Flask, request as flask_request

MiddlewareType = Enum('MiddlewareType', ('Request', 'Response'))


class Middleware:

    func = Callable
    tag = str
    weight = int
    type = MiddlewareType

    def __init__(
            self,
            func: Callable,
            tag: str = None,
            weight: int = 0,
            m_type: MiddlewareType = MiddlewareType.Request
    ):
        self.func = func
        self.tag = tag
        self.weight = weight
        self.type = m_type


class Module:
    name = str
    __registered_function = bool
    __middleware = dict
    __function = dict

    def __init__(self, name: str):
        self.name = name
        self.__middleware = {
            '': list()
        }
        self.__function = dict()
        self.__registered_function = False

    def register_middleware(self, middleware: Middleware) -> None:
        if self.__registered_function:
            raise Exception('Can\'t register middleware after called function')
        if middleware.tag is None:
            self.__middleware[''].append(middleware)
        else:
            if middleware.tag not in self.__middleware.keys():
                self.__middleware[middleware.tag] = list()
            self.__middleware[middleware.tag].append(middleware)

    def request(self, request):
        if request.function not in self.__function.keys():
            raise Exception('function not found')
        all_middleware = list()
        for middleware in self.__middleware['']:
            all_middleware.append(middleware)
        req_func = self.__function[request.function]
        if req_func.tags is not None:
            for tag in req_func.tags:
                for middleware in self.__middleware[tag]:
                    all_middleware.append(middleware)
        all_middleware.sort(key=lambda mid: mid.weight, reverse=True)
        for middleware in all_middleware:
            if middleware.type != MiddlewareType.Request:
                continue
            new_request = middleware.func(request)
            if new_request is not None:
                request = new_request
        request.response = req_func.f(**request.args)
        for middleware in all_middleware:
            if middleware.type != MiddlewareType.Response:
                continue
            new_response = middleware.func(request.response)
            if new_response is not None:
                request.response = new_response

    def function(self, name: str, tags: list = None):
        def decorator(f):
            self.__registered_function = True
            self.__function[name] = _ModuleFunction(f=f, tags=tags)
            return f

        return decorator


class _ModuleFunction:
    f = Callable
    tags = list

    def __init__(self, f: Callable, tags: list = None):
        self.f = f
        self.tags = tags


class Error(BaseException):
    code = int
    message = str

    def __init__(self, code: int = 0, msg: str = ''):
        self.code = code
        self.message = msg


class Response:
    data = dict
    error = Error

    def __init__(self, data: (dict, list) = None, error: Error = None) -> None:
        if data is None:
            self.data = dict()
        else:
            self.data = data
        if error is None:
            self.error = Error()
        else:
            self.error = error

    @property
    def response(self) -> str:
        return json.dumps(dict(data=self.data, error=self.error), cls=ResponseEncoder)


class Request:
    module = Module
    function = str
    args = dict
    response = Response

    def __init__(self, req: dict):
        if 'module' not in req.keys() or 'function' not in req.keys() or 'args' not in req.keys():
            raise Exception('wrong request arguments')
        self.module = App.get_instance().get_module(req['module'])
        self.function = req['function']
        self.args = req['args']
        self.module.request(self)


class ResponseEncoder(json.JSONEncoder):

    def default(self, o: Any) -> Any:
        if isinstance(o, Error):
            return dict(code=o.code, msg=o.message)
        return json.JSONEncoder.default(self, o)


class App(Flask):
    __instance = None
    __modules = dict

    def __init__(self, name: str = 'lazy_flask', endpoint: str = '/query'):
        super().__init__(name)
        self.__modules = dict()
        self.__instance.add_url_rule(endpoint, None, App.query, methods=['POST'])

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def register_module(self, module: Module) -> None:
        self.__modules[module.name] = module

    def get_module(self, name: str) -> Module:
        if name not in self.__modules.keys():
            raise Exception('{} not in modules'.format(name))
        return self.__modules[name]

    @staticmethod
    def query():
        try:
            req = Request(flask_request.json)
            return req.response.response
        except Error as e:
            return Response(error=e).response

    @staticmethod
    def get_instance():
        return App.__instance
