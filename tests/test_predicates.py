import marshmallow
import pytest
from pyramid import testing


class ValueSchema(marshmallow.Schema):
    value = marshmallow.fields.Integer(required=True)


@pytest.mark.parametrize(
    "schema_content_type, request_content_type, request_extra",
    [
        (
            "application/json",
            "application/json",
            dict(json={"value": 1}),
        ),
        pytest.param(
            "application/json",
            "application/x-www-urlencoded",
            dict(params={"value": "1"}),
            marks=pytest.mark.xfail(strict=True),
        ),
        (
            "application/json",
            "application/json;charset=utf8",
            dict(json={"value": 1}),
        ),
        (
            "application/x-www-form-urlencoded",
            "application/x-www-form-urlencoded",
            dict(params={"value": "1"}),
        ),
        (
            "multipart/form-data",
            "multipart/form-data",
            dict(params={"value": "1"}),
        ),
        pytest.param(
            "multipart/form-data",
            "application/json;charset=utf8",
            dict(json={"value": 1}),
            marks=pytest.mark.xfail(strict=True),
        ),
    ],
)
def test_request_body_schema_predicate(
    schema_content_type,
    request_content_type,
    request_extra,
):
    from rebecca.apispec.predicates import RequestBodySchemaPredicate

    context = testing.DummyResource()
    request = testing.DummyRequest(
        content_type=request_content_type,
        **request_extra,
    )
    predicate = RequestBodySchemaPredicate(
        {
            schema_content_type: {
                "schema": ValueSchema(),
            },
        },
        {},
    )
    result = predicate(context, request)
    assert result
    assert request.data == {"value": 1}
