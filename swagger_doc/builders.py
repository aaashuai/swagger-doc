import collections
import logging
import os
import queue
import re
import typing
from inspect import getfullargspec

import tornado.web
import yaml
from jinja2 import BaseLoader
from jinja2 import Environment
from tornado.web import URLSpec

if typing.TYPE_CHECKING:
    from .models import SSecurity, DocModel

SWAGGER_TEMPLATE = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "swagger.yaml"))
replace_symbols = {"/", "$", "(", ")", "{", "}"}
replace_map = {ord(k): v for k, v in dict(zip(replace_symbols, ["_"] * len(replace_symbols))).items()}


def build_doc_from_func_doc(handler, route_path, security: "SSecurity"):
    out = {}

    for method in handler.SUPPORTED_METHODS:
        method = method.lower()
        swagger: "DocModel" = getattr(getattr(handler, method), "__swagger__", None)
        if swagger:
            d = swagger.gen_doc()
            d["operationId"] = f"{method}_{handler.__name__}_{route_path.translate(replace_map)}"
            if swagger.auth_required and security:
                d["security"] = security.get_security()
            out.update({method: d})

    return out


def try_extract_docs(method_handler):
    try:
        if hasattr(method_handler, "__wrapped__"):
            return try_extract_docs(method_handler.__wrapped__)
        return getfullargspec(method_handler).args[1:]
    except TypeError:  # unsupported callable
        return []


def extract_parameters_names(handler, parameters_count):
    if parameters_count == 0:
        return []

    parameters = ["{?}" for _ in range(parameters_count)]

    for method in handler.SUPPORTED_METHODS:
        method_handler = getattr(handler, method.lower())
        args = try_extract_docs(method_handler)

        if len(args) > 0:
            for i, arg in enumerate(args):
                if set(arg) != {"_"}:
                    try:
                        parameters[i] = arg
                    except:
                        logging.warning(f"{handler.__name__} {method} 参数传递有误")

    return parameters


def format_handler_path(target, route_pattern, groups):
    brackets_regex = re.compile(r"\(.*?\)")
    parameters = extract_parameters_names(target, groups)

    for i, entity in enumerate(brackets_regex.findall(route_pattern)):
        route_pattern = route_pattern.replace(entity, "{%s}" % parameters[i], 1)

    return route_pattern[:-1]


def dict2yaml(d, indent=10, result=""):
    for key, value in d.items():
        result += " " * indent + str(key) + ":"
        if isinstance(value, dict):
            result = dict2yaml(value, indent + 2, result + "\n")
        else:
            result += " " + str(value) + "\n"
    return result


def generate_doc_from_endpoints(
    routes,
    servers,
    description,
    api_version,
    title,
    contact,
    external_docs,
    security: "SSecurity",
):
    # Clean description
    _start_desc = 0
    for i, word in enumerate(description):
        if word != "\n":
            _start_desc = i
            break
    cleaned_description = "    ".join(description[_start_desc:].splitlines())

    # Load base Swagger template
    jinja2_env = Environment(loader=BaseLoader())
    jinja2_env.filters["nesteddict2yaml"] = dict2yaml

    with open(SWAGGER_TEMPLATE, "r") as f:
        swagger_base = jinja2_env.from_string(f.read()).render(
            description=cleaned_description,
            version=api_version,
            title=title,
            contact=contact,
            servers=servers,
            external_docs=external_docs,
        )

    # The Swagger OBJ
    swagger = yaml.safe_load(swagger_base)
    swagger["paths"] = collections.defaultdict(dict)
    swagger["components"] = {}
    swagger["servers"] = servers

    if security:
        swagger["components"]["securitySchemes"] = security.get_security_schema()

    q = queue.Queue()
    for route in routes:
        q.put(route)

    while not q.empty():
        item = q.get()
        if isinstance(item, URLSpec):
            route = item
        elif isinstance(item, tuple):
            _, left = item
            if isinstance(left, list):
                for item in left:
                    q.put(item)
                continue
            else:
                route = tornado.web.url(*item)
        else:
            raise ValueError(f"Unknown route: {item}")

        target = route.target
        if not target:
            continue

        route_path = format_handler_path(target, route.regex.pattern, route.regex.groups)
        doc = build_doc_from_func_doc(target, route_path, security)
        if not doc:
            continue
        swagger["paths"][route_path].update(doc)

    return swagger
