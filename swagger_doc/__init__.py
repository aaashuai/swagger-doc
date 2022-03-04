__version__ = "0.0.7"

import importlib
import json
import os
from enum import Enum
from pathlib import Path
from typing import List, Type, Union

import tornado.web

from .builders import generate_doc_from_endpoints
from .handlers import *
from .models import *
from .utils import CJsonEncoder

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger_ui"))


def export_swagger(
    routes,
    servers=None,
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    external_docs=None,
    security=None,
):
    return generate_doc_from_endpoints(
        routes,
        servers=servers,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        external_docs=external_docs,
        security=security,
    )


def setup_swagger(
    routes,
    swagger_url="/docs",
    openapi_url="/openapi.json",
    servers=None,
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    external_docs=None,
    security: SSecurity = None,
    login_username: str = "swagger",
    login_password: str = "swagger",
    swagger_model_path=None,
):
    swagger_schema = generate_doc_from_endpoints(
        routes,
        servers=servers,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        external_docs=external_docs,
        security=security,
    )

    _swagger_url = "/{}".format(swagger_url) if not swagger_url.startswith("/") else swagger_url
    _openapi_url = "/{}".format(openapi_url) if not openapi_url.startswith("/") else openapi_url
    _base_swagger_url = _swagger_url.rstrip("/")

    routes += [
        tornado.web.url(_swagger_url, SwaggerHomeHandler),
        tornado.web.url(_openapi_url, OpenapiHomeHandler),
        tornado.web.url("{}/".format(_base_swagger_url), SwaggerHomeHandler),
    ]
    with open(os.path.join(STATIC_PATH, "swagger-ui-bundle.js"), "r") as f:
        swagger_ui_bundle_js = f.read()

    with open(os.path.join(STATIC_PATH, "swagger-ui-standalone-preset.js"), "r") as f:
        swagger_ui_standalone_preset_js = f.read()

    with open(os.path.join(STATIC_PATH, "swagger-ui.css"), "r") as f:
        swagger_ui_css = f.read()

    with open(os.path.join(STATIC_PATH, "ui.jinja2"), "r") as f:
        SwaggerHomeHandler.SWAGGER_HOME_TEMPLATE = (
            f.read()
            .replace("{{ SWAGGER_SCHEMA }}", json.dumps(swagger_schema, cls=CJsonEncoder))
            .replace("{{ SWAGGER-CSS }}", swagger_ui_css)
            .replace("{{ SWAGGER-UI-BUNDLE }}", swagger_ui_bundle_js)
            .replace("{{ SWAGGER-UI-STANDALONE-PRESET }}", swagger_ui_standalone_preset_js)
        )
    OpenapiHomeHandler.SWAGGER_JSON = swagger_schema
    SwaggerUser.USERNAME = login_username
    SwaggerUser.PASSWORD = login_password


def load_swagger(swagger_model_path=None):
    """注册schema的时候使用, 暂时无用"""
    if not swagger_model_path:
        path = str((Path(__file__).parent / "models").absolute())
    else:
        path = Path(swagger_model_path)

    import_base_name = Path(__file__).absolute().parent.parent.name
    for root, _, files in os.walk(path):
        for file in files:
            if file.startswith("_") or not file.endswith(".py"):
                continue

            import_module = ".".join(
                [
                    import_base_name,
                    *root.split(import_base_name)[1].split(os.path.sep)[1:],
                    file[:-3],
                ]
            )
            importlib.import_module(import_module)


def swagger_doc(
    tags: List[Union[str, Enum]],
    summary: str,
    responses: List[SResponse],
    desc: str = None,
    request_body: Type[SBody] = None,
    path_params: Type[SPath] = None,
    query_params: Type[SQuery] = None,
    header_params: Type[SHeader] = None,
    auth_required: bool = True,
):
    def wrapper(func):
        func.__swagger__ = DocModel(
            tags=tags,
            summary=summary,
            desc=desc or summary,
            responses=responses,
            request_body=request_body,
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            auth_required=auth_required,
        )
        return func

    return wrapper
