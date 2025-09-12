# coding=utf-8

import requests

url = "http://localhost:9000/query"

hello_data = {"module": "api", "function": "hello", "args": {"word": "world"}}
tag_data = {"module": "api", "function": "tag", "args": {}}
error_data = {"module": "api", "function": "error", "args": {}}

res = requests.post(url, json=hello_data)
print(res.json())

res = requests.post(url, json=tag_data)
print(res.json())

res = requests.post(url, json=error_data)
print(res.json())
