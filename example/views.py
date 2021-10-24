from pyramid.view import view_config
from . import schema


@view_config(
    route_name="api.index",
    renderer="json",
    request_method="GET",
    query_schema=schema.DocumentSearchSchema(),
    responses_schema=schema.DocumentListSchema(),
)
def index(request):
    """api index"""
    return {}


@view_config(
    route_name="api.index",
    renderer="json",
    request_method="POST",
    request_body_schema=schema.DocumentSchema(),
    responses_schema=schema.DocumentSchema(),
)
def create(request):
    """create document api"""
    return {}


@view_config(
    route_name="api.upload",
    renderer="json",
    request_method="POST",
    request_body_schema={
        "multipart/form-data": {
            "schema": schema.UploadSchema(),
        },
    },
    responses_schema=schema.DocumentSchema(),
)
def upload(request):
    """upload api"""
    return {}
