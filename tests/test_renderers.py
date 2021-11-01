import marshmallow
import pytest
from pyramid import testing


class ValueSchema(marshmallow.Schema):
    value = marshmallow.fields.Integer(required=True)


@pytest.mark.parametrize(
    "status_code,content_type,response_body",
    [
        (200, "application/json", '{"value": 1}'),
        (200, "application/json;charset=utf8", '{"value": 1}'),
        (200, "application/x-www-form-urlencoded", "value=1"),
        (201, "application/json", '{"value": 1}'),
    ]
)
def test_render_schema(status_code, content_type, response_body):
    from rebecca.apispec.renderers import SchemaRenderer

    apispec = {
        "response_schemas": {
            "default": {
                "content": {
                    "application/json": {
                        "schema": ValueSchema(),
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": ValueSchema(),
                    },
                },
            },
        },
    }
    request = testing.DummyRequest(
        apispec_schemas=apispec,
    )
    request.response.status_int = status_code
    request.response.content_type = content_type
    system = {
        "request": request,
    }
    renderer = SchemaRenderer({})
    result = renderer({"value": 1, "additional": "a"}, system)
    assert result == response_body
