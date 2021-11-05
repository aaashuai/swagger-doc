# SwaggerDoc   

[![Python](https://img.shields.io/badge/Python-3.4+-blue.svg)](https://python.org/)
[![Tornado](https://img.shields.io/badge/Tornado-6.0.1+-blue.svg)](https://python.org/)

## About
swagger tool for tornado

## Installation
`pip install swagger-doc`

## Quick Start
### code
```python
import tornado.ioloop
import tornado.web

from pydantic import Field
from swagger_doc import setup_swagger, swagger_doc, SResponse200, STag, SObject


class SwaggerTag(STag):
    home = "home"
    
    
class SuccessResp(SObject):
    __example__ = {"code": "0"}

    code: str = Field(description="response code")


class MainHandler(tornado.web.RequestHandler):
    @swagger_doc(
        tags=[SwaggerTag.home],
        summary="show home page",
        responses=[SResponse200(body=Resp)],
    )
    def get(self):
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
    return AppWithSwagger([(r"/", MainHandler)])


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
<img src="https://user-images.githubusercontent.com/39478406/140527529-140c33ba-a9b0-48d0-b880-62cbfed4842a.png" width="455px" alt="wechaty" />

## Examples
see [examples](https://github.com/aaashuai/swagger-doc/tree/master/examples)

## TODO
1. other response(only support json response currently)
2. ...
