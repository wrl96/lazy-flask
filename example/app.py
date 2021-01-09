# coding=utf-8

from lazy_flask import *

app = App()

api = Module('api')
App.get_instance().register_module(api)


def req_middleware_1(req: Request):
    print('Request middleware 1')


def req_middleware_2(req: Request):
    print('Request middleware 2')


def req_middleware_3(req: Request):
    print('Request middleware 3')
    req.args['middleware'] = True
    return req


def resp_middleware_1(resp: Response):
    print('Response middleware 1')


api.register_middleware(Middleware(req_middleware_1, weight=1))
api.register_middleware(Middleware(req_middleware_2, weight=2))
api.register_middleware(Middleware(req_middleware_3, tag='update'))
api.register_middleware(Middleware(resp_middleware_1, m_type=MiddlewareType.Response))


@api.function('hello')
def hello(word: str = ''):
    return Response(data={'hello': word})


@api.function('tag', tags=['update'])
def tag(middleware: bool = False):
    return Response(data={'middleware': middleware})


@api.function('error')
def error():
    return Response(error=Error(code=1, msg='Error!'))


app.run(host='0.0.0.0', port=9000)
