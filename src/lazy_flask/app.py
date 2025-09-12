import json

from typing import Optional, ClassVar
from flask import Flask, request as flask_request, Response as FlaskResponse
from lazy_core import APIRequest, APIResponse, APIError, APIException, LazyApp


class App(Flask, LazyApp):
    _instance: ClassVar[Optional["App"]] = None
    _initialized: bool = False

    def __init__(self, name: str = "lazy_flask", endpoint: str = "/query"):
        if not self._initialized:
            Flask.__init__(self, name)
            LazyApp.__init__(self)
            self.add_url_rule(endpoint, "api", self.handle_request, methods=["POST"])
            self._initialized = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def handle_request(self) -> FlaskResponse:
        try:
            request_data = flask_request.get_json()
            request = APIRequest.from_dict(request_data)

            module = self.get_module(request.module_name)
            module.request(request)
            if request.response is None:
                request.response = APIResponse()

            return FlaskResponse(
                response=json.dumps(request.response.formatted, cls=self.json_encoder),
                status=200,
                mimetype="application/json",
            )
        except APIException as e:
            return FlaskResponse(
                response=json.dumps(APIResponse(error=e.error).formatted),
                status=200,
                mimetype="application/json",
            )
        except Exception as e:
            error = APIError(code=500, message=str(e))
            return FlaskResponse(
                response=json.dumps(APIResponse(error=error).formatted),
                status=500,
                mimetype="application/json",
            )
