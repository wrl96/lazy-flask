# Lazy_flask
lazy_flask是一个基于flask的懒人开发框架，可省去设计API的时间，快速构建小项目的后端。

特性：

- 基于Flask二次封装，支持所有Flask特性
- 代码量小，仅不到200行
- 支持插入自定义中间件

## 快速开始

#### 初始化
```python
from lazy_flask import App

app = App(name='lazy_flask', endpoint='/query')
```
|参数|类型|默认值|备注|
|---|---|---|---|
|name|str|lazy_flask|flask应用名称，随意|
|endpoint|str|/query|交互端点|

#### 注册模块
```python
from lazy_flask import App, Module

module = Module('module')
App.get_instance().register_module(module)
```
Module

|参数|类型|默认值|备注|
|---|---|---|---|
|name|str| |模块名称，不可重复|

register_module

|参数|类型|默认值|备注|
|---|---|---|---|
|module|Module| |向App注册该模块|

#### 注册函数
```python
from lazy_flask import App, Module, Response, Error

@module.function('hello')
def hello(name: str = '') -> Response:
    return Response(data={'hello': name})

@module.function('oh')
def oh() -> Response:
    return Response(error=Error(code=1, msg='This is an error.'))
```
function

|参数|类型|默认值|备注|
|---|---|---|---|
|name|str| |函数名称，同一模块内不可重复|

Response

|参数|类型|默认值|备注|
|---|---|---|---|
|data|dict|{}|返回的数据|
|error|Error|Error()|错误信息|

Error

|参数|类型|默认值|备注|
|---|---|---|---|
|code|int|0|错误码|
|msg|str| |错误提示|

#### 发起请求

```python
import requests

url = "http://{host}/query"

data = {
    "module": "module", 
    "function": "hello", 
    "args": {
        "name": "world"
    }
}

response = requests.request("POST", url, json=data)

print(response.text) # {"data": {"hello": "world"}, "error": {"code": 0, "msg": ""}}
```

## 高级用法

#### 中间件

中间件可以拦截请求，在请求到达处理函数之前/返回请求结果之前做一些事情，例如权限校验<br>
你只需要定义一个函数，接收Request/Response参数即可获取相应的值<br>
如果你想修改请求/响应，请在中间件函数中修改，并返回新的request/response，如果不返回，lazy_flask将继续使用传入的值


```python
# 权限校验
import time

from lazy_flask import *
from flask import request as flask_request

info = Module('info')
App.get_instance().register_module(info)

# 检查request，只有tag含有login时执行
def login_middleware(request: Request):
    user_id = request.args.get('id', None)
    if user_id is None:
        raise Error(code=1, msg='User id is none')
    token = flask_request.headers.get('Authorization', None)
    if token is None:
        raise Error(code=2, msg='Token is none')

info.register_middleware(Middleware(login_middleware, tag='login', weight=1, type=MiddlewareType.Request))

# 修改response，全局执行
def add_timestamp_middleware(response: Response) -> Response:
    response['timestamp'] = int(time.time() * 1000)
    return response

info.register_middleware(Middleware(add_timestamp_middleware, type=MiddlewareType.Response))

@info.function('info', tags=['login'])
def info():
    return Response(data={'result': 'ok'})
```

Middleware

|参数|类型|默认值|备注|
|---|---|---|---|
|function|Callable| |中间件处理函数，需要接收Request或Response|
|tag|str| |标签，设置后需要在装饰器中显式指定相同的标签才会执行，否则全局执行|
|weight|int|1|优先级，越大越早执行|
|type|MiddlewareType|MiddlewareType.Request|中间件类型，表示是请求中间件还是响应中间件|

## Demo

```python
pip3 install dist/lazy_flask-0.0.1.tar.gz
pip3 install requests

python3 example/app.py
python3 example/req.py # 新开一个终端
```
