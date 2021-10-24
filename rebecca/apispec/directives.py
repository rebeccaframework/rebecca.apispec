from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from pyramid.urldispatch import route_re

from . import predicates


def add_apispec(config, title, version):
    config.registry["apispec_config"] = dict(
        title=title,
        version=version,
        openapi_version="3.0.2",
    )


def get_apispec(request):
    introspector = request.registry.introspector
    routes = get_routes(request)
    apispec = APISpec(
        **request.registry["apispec_config"],
        plugins=(MarshmallowPlugin(),),
    )
    for route in routes:
        path_params = [
            {
                "name": p[0].strip("{}"),
                "in": "path",
                "schema": {"type": "string"},
                "required": True,
            }
            for p in route_re.finditer(route["introspectable"]["pattern"])
        ]
        operations = {}
        for v in introspector.related(route["introspectable"]):
            if v.category_name == "views":
                if not v["request_methods"]:
                    continue
                doc = v["callable"].__doc__
                if doc and "\n" in doc:
                    doc = doc.split("\n", 1)[0]
                operation = {
                    "parameters": [],
                    "summary": doc,
                }
                operation["parameters"] = operation["parameters"] + path_params
                for p in v["predicates"]:
                    if isinstance(p, predicates.RequestBodySchemaPredicate):
                        operation["requestBody"] = {
                            "content": p.content,
                        }
                    elif isinstance(p, predicates.ResponsesSchemaPredicate):
                        operation["responses"] = p.content
                    elif isinstance(p, predicates.QuerySchemaPredicate):
                        operation["parameters"].append({
                            "in": "query",
                            "schema": p.schema,
                        })
                operations[v["request_methods"].lower()] = operation
        if operations:
            apispec.path(
                "/" + route["introspectable"]["pattern"].lstrip("/"),
                operations=operations,
            )
    return apispec


def get_routes(request):
    introspector = request.registry.introspector
    return introspector.get_category("routes")
