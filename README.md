# SwaggerDoc   

[![Python](https://img.shields.io/badge/Python-3.4+-blue.svg)](https://python.org/)
[![Tornado](https://img.shields.io/badge/Tornado-6.0.1+-blue.svg)](https://python.org/)

## About
A swagger tool for tornado, using python to write api doc!

## Installation
`pip install swagger-doc`

## Quick Start
### code
```python
import tornado.ioloop
import tornado.web

from pydantic import Field
from swagger_doc import setup_swagger, swagger_doc, SResponse200, SResponse401, STag, SObject, SPath, SQuery, SBody


class SwaggerTag(STag):
    home = "home"


class RequestPath(SPath):
    __example__ = {"id": 111}

    id: int = Field(description="id")


class RequestQuery(SQuery):
    __example__ = {"page": 10}

    page: int = Field(description="page")


class RequestBody(SBody):
    __example__ = {"name": "lisi"}

    name: str = Field(description="name")

    
class SuccessResp(SObject):
    __example__ = {"code": "0"}

    code: str = Field(description="response code")


class UnauthorizedResp(SObject):
    __example__ = {"code": 401}


class MainHandler(tornado.web.RequestHandler):
    @swagger_doc(
        tags=[SwaggerTag.home],
        summary="show home page",
        query_params=RequestQuery,
        path_params=RequestPath,
        request_body=RequestBody,
        responses=[SResponse200(body=SuccessResp), SResponse401(body=UnauthorizedResp)],
    )
    def post(self, id_):
        self.write("Hello, world")


class AppWithSwagger(tornado.web.Application):
    def __init__(self, routes, *args, **kwargs):
        setup_swagger(
            routes,
            swagger_url="/docs",
            openapi_url="/openapi.json",
            description="",
            api_version="1.0.0",
            title="API DOCS.",
        )
        super().__init__(routes, *args, **kwargs)


def make_app():
    return AppWithSwagger([(r"/(\d+)", MainHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8885)
    print(f"docs: http://localhost:8885/docs")
    tornado.ioloop.IOLoop.current().start()
```

### Authroization  
default account&password: swagger:swagger  
<img src="https://user-images.githubusercontent.com/39478406/140527121-d282c21b-1b21-4fa4-ae43-c37bef114d2e.png" width="455px" alt="wechaty" />

### Docs  
<img src="https://user-images.githubusercontent.com/39478406/140530562-390734ba-0d6e-4eaf-8998-9fac8d16092e.png" width="455px" alt="wechaty" />

## Examples
see [examples](https://github.com/aaashuai/swagger-doc/tree/master/examples)

## TODO
1. other response(only support json response currently)
2. search bar
3. ...
