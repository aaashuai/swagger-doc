import tornado.ioloop
import tornado.web

from models import (
    SwaggerTag,
    UnauthorizedResp,
    SuccessResp,
    RequestEnum,
    RequestEnumQuery,
)
from swagger_doc import setup_swagger, swagger_doc, SResponse200, SResponse401


class EnumHandler(tornado.web.RequestHandler):
    @swagger_doc(
        tags=[SwaggerTag.form],
        summary="enum test",
        query_params=RequestEnumQuery,
        request_body=RequestEnum,
        responses=[SResponse200(body=SuccessResp), SResponse401(body=UnauthorizedResp)],
    )
    def post(self):
        params = RequestEnumQuery.model_validate_json(self.request.body)
        self.write(params.model_dump_json())


class AppWithSwagger(tornado.web.Application):
    def __init__(self, routes, *args, **kwargs):
        setup_swagger(
            routes,
            swagger_url="/docs",
            openapi_url="/openapi.json",
            description="",
            api_version="1.0.0",
            title="IVMS TEAM API DOCS.",
        )
        super().__init__(routes, *args, **kwargs)


def make_app():
    return AppWithSwagger(
        [
            (r"/enum", EnumHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8887)
    print(f"docs: http://localhost:8887/docs")
    print(f"docs: http://localhost:8887/redoc")
    tornado.ioloop.IOLoop.current().start()
