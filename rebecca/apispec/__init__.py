from . import directives, predicates

SWAGGER_UI_VERSION = "3.52.3"


def includeme(config):
    config.add_directive("add_apispec", directives.add_apispec)
    config.add_directive("get_apispec", directives.get_apispec)
    config.add_request_method(directives.get_apispec, "apispec", reify=True)
    config.add_view_predicate(
        "request_body_schema",
        predicates.RequestBodySchemaPredicate,
    )
    config.add_view_predicate(
        "responses_schema",
        predicates.ResponsesSchemaPredicate,
    )
    config.add_view_predicate(
        "query_schema",
        predicates.QuerySchemaPredicate,
    )
    config.add_route("apispec.swagger-json", "/swagger.json")
    config.add_static_view(
        name="apispec.swaggerui",
        path=f"{__name__}:static/swagger-ui-{SWAGGER_UI_VERSION}",
    )
    config.add_static_view(
        name="apispec.redoc",
        path=f"{__name__}:static/redoc",
    )
    config.scan(".views")
