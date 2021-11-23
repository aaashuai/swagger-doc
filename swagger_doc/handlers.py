import base64
import functools
import json

import tornado.web

from .utils import CJsonEncoder

__all__ = [
    "TornadoHandler",
    "SwaggerHomeHandler",
    "OpenapiHomeHandler",
    "SwaggerUser",
]


class SwaggerUser:
    USERNAME = None
    PASSWORD = None


def api_auth(username, password):
    if username == SwaggerUser.USERNAME and password == SwaggerUser.PASSWORD:
        return True
    return False


def basic_auth(auth):
    def decorator(f):
        def _request_auth(handler):
            handler.set_header("WWW-Authenticate", "Basic realm=JSL")
            handler.set_status(401)
            handler.finish()

        @functools.wraps(f)
        def new_f(*args):
            handler = args[0]

            auth_header = handler.request.headers.get("Authorization")
            if auth_header is None:
                return _request_auth(handler)
            if not auth_header.startswith("Basic "):
                return _request_auth(handler)

            auth_decoded = base64.decodebytes(auth_header[6:].encode("utf8")).decode("utf8")
            username, password = auth_decoded.split(":", 2)

            if auth(username, password):
                f(*args)
            else:
                _request_auth(handler)

        return new_f

    return decorator


class TornadoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class SwaggerHomeHandler(TornadoHandler):
    SWAGGER_HOME_TEMPLATE = ""

    @basic_auth(api_auth)
    def get(self):
        self.write(self.SWAGGER_HOME_TEMPLATE)


class OpenapiHomeHandler(TornadoHandler):
    SWAGGER_JSON = ""

    @basic_auth(api_auth)
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(self.SWAGGER_JSON, ensure_ascii=False, cls=CJsonEncoder).replace("</", "<\\/"))
