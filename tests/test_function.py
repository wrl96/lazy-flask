import json
import unittest
from lazy_flask import *


class TestAPIClass(unittest.TestCase):

    def test_api_request(self):
        data = {'module': 'math', 'function': 'add'}
        req = APIRequest(data)
        self.assertEqual(req.module_name, 'math')
        data = {'module': 'math'}
        with self.assertRaises(ValueError):
            APIRequest(data)

    def test_api_response(self):
        response = APIResponse(data={'key': 'value'})
        self.assertIn('key', response.formatted['data'])


class TestLazyFlask(unittest.TestCase):

    def setUp(self):
        # 初始化应用和模块
        self.app = App()
        self.client = self.app.test_client()

    def test_request_processing_flow(self):
        # 注册测试模块
        self.middleware = Middleware(func=lambda req: req, weight=1, tag='test')
        self.resp_middleware = Middleware(func=lambda resp: resp, m_type=MiddlewareType.Response)
        self.module = Module('test')
        self.module.register_middleware(self.middleware)
        self.module.register_middleware(self.resp_middleware)

        @self.module.function('demo', tags=['test'])
        def demo_func():
            return APIResponse(data={'result': 'ok'})

        self.app.register_module(self.module)
        # 测试完整的请求处理流程
        response = self.client.post('/query', json={
            'module': 'test',
            'function': 'demo'
        })
        self.assertEqual(response.status_code, 200)

    def test_request_processing_flow_error(self):
        self.module = Module('test_error')

        @self.module.function('demo')
        def demo_func():
            raise APIError(code=1, message='Error!')
        self.app.register_module(self.module)
        response = self.client.post('/query', json={
            'module': 'test_error',
            'function': 'demo'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_duplicate_module(self):
        # 测试重复注册模块
        self.module = Module('duplicate_module')
        self.app.register_module(self.module)
        with self.assertRaises(ValueError):
            self.app.register_module(self.module)

    def test_register_duplicate_middleware(self):
        # 测试重复注册中间件
        self.module = Module('duplicate_middleware')
        self.middleware = Middleware(func=lambda req: req, weight=1)
        self.module.register_middleware(self.middleware)

        @self.module.function('demo')
        def demo_func():
            return APIResponse(data={'result': 'ok'})

        with self.assertRaises(RuntimeError):
            self.module.register_middleware(self.middleware)

    def test_request_function(self):
        self.module = Module('test_request')
        self.app.register_module(self.module)
        response = self.client.post('/query', json={
            'module': 'test_request_1',
            'function': 'demo'
        })
        self.assertEqual(response.status_code, 500)
        response = self.client.post('/query', json={
            'module': 'test_request',
            'function': 'demo1'
        })
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
