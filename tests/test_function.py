import pytest
from lazy_flask import (
    Module,
    Middleware,
    MiddlewareType,
    App,
    APIResponse,
    APIException,
    APIError,
)


@pytest.fixture(autouse=True)
def setup_app():
    app = App()
    client = app.test_client()
    return app, client


def test_request_processing_flow(setup_app):
    app, client = setup_app
    middleware = Middleware(func=lambda req: req, priority=1, tag="test")
    resp_middleware = Middleware(func=lambda resp: resp, m_type=MiddlewareType.Response)
    module = Module("test")
    module.register_middleware(middleware)
    module.register_middleware(resp_middleware)

    @module.function("demo", tags=["test"])
    def demo_func():
        return APIResponse(data={"result": "ok"})

    app.register_module(module)
    response = client.post("/query", json={"module": "test", "function": "demo"})
    assert response.status_code == 200


def test_request_processing_flow_error(setup_app):
    app, client = setup_app
    module = Module("test_error")

    @module.function("demo")
    def demo_func():
        raise APIException(error=APIError(code=1, message="Error!"))

    app.register_module(module)
    response = client.post("/query", json={"module": "test_error", "function": "demo"})
    assert response.status_code == 200


def test_register_duplicate_module(setup_app):
    app, _ = setup_app
    module = Module("duplicate_module")
    app.register_module(module)
    with pytest.raises(ValueError):
        app.register_module(module)


def test_register_duplicate_middleware():
    module = Module("duplicate_middleware")
    middleware = Middleware(func=lambda req: req, priority=1)
    module.register_middleware(middleware)

    @module.function("demo")
    def demo_func():
        return APIResponse(data={"result": "ok"})

    with pytest.raises(RuntimeError):
        module.register_middleware(middleware)


def test_request_function(setup_app):
    app, client = setup_app
    module = Module("test_request")
    app.register_module(module)
    response = client.post(
        "/query", json={"module": "test_request_1", "function": "demo"}
    )
    assert response.status_code == 500
    response = client.post(
        "/query", json={"module": "test_request", "function": "demo1"}
    )
    assert response.status_code == 500
