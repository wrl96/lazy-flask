# coding=utf-8

from lazy_flask import (
    App,
    Module,
    Middleware,
    MiddlewareType,
    APIRequest,
    APIResponse,
    APIError,
)

app = App()

api = Module("api")
app.register_module(api)


def req_middleware_1(req: APIRequest):
    print("Request middleware 1")


def req_middleware_2(req: APIRequest):
    print("Request middleware 2")


def req_middleware_3(req: APIRequest):
    print("Request middleware 3")
    req.args["middleware"] = True
    return req


def resp_middleware_1(resp: APIResponse):
    print("Response middleware 1")


api.register_middleware(Middleware(func=req_middleware_1, priority=1))
api.register_middleware(Middleware(func=req_middleware_2, priority=2))
api.register_middleware(Middleware(func=req_middleware_3, tag="update"))
api.register_middleware(
    Middleware(func=resp_middleware_1, m_type=MiddlewareType.Response)
)


@api.function("hello")
def hello(word: str = ""):
    return APIResponse(data={"hello": word})


@api.function("tag", tags=["update"])
def tag(middleware: bool = False):
    return APIResponse(data={"middleware": middleware})


@api.function("error")
def error():
    return APIResponse(error=APIError(code=1, message="Error!"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
