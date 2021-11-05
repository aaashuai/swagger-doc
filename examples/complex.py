import tornado.ioloop
import tornado.web

from models import SwaggerTag, RequestQuery, RequestBody, RequestPath, UnauthorizedResp, SuccessResp
from swagger_doc import setup_swagger, swagger_doc, SResponse200, SResponse401


class MainHandler(tornado.web.RequestHandler):
    @swagger_doc(
        tags=[SwaggerTag.home],
        summary="show home page",
        query_params=RequestQuery,
        path_params=RequestPath,
        request_body=RequestBody,
        responses=[SResponse200(body=SuccessResp), SResponse401(body=UnauthorizedResp)],
    )
    def put(self, id_):
        self.write("Hello, world")


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
    return AppWithSwagger([(r"/", MainHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8887)
    print(f"docs: http://localhost:8887/docs")
    tornado.ioloop.IOLoop.current().start()
