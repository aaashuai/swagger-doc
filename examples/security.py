import tornado.ioloop
import tornado.web

from models import Resp, swagger_security, SwaggerTag
from swagger_doc import setup_swagger, swagger_doc, SResponse200


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
            title="IVMS TEAM API DOCS.",
            security=swagger_security,
        )
        super().__init__(routes, *args, **kwargs)


def make_app():
    return AppWithSwagger([(r"/", MainHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8886)
    print(f"docs: http://localhost:8886/docs")
    tornado.ioloop.IOLoop.current().start()
