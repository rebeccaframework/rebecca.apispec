import marshmallow
import pyramid.request
from pyramid import testing


class DummySchema(marshmallow.Schema):
    title = marshmallow.fields.String()
    value = marshmallow.fields.Integer()


class DummyResponseSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer()
    title = marshmallow.fields.String()
    value = marshmallow.fields.Integer()


def test_it():
    with testing.testConfig() as config:
        config.include("rebecca.apispec")
        config.add_apispec("test API", "0.1+test")
        config.add_route("test.api1", "/v1/api1")
        config.add_route("test.api2", "v1/api2/{id}")

        def get_api1(request):
            """get api1 resource
            ---
            # this is api1
            """
            return request.response

        def post_api1(request):
            """create api1 resource"""
            return request.response

        config.add_view(
            get_api1,
            route_name="test.api1",
            request_method="GET",
        )
        config.add_view(
            lambda request: request.response,
            route_name="test.api2",
            request_method="GET",
            responses_schema=DummyResponseSchema(),
        )
        config.add_view(
            post_api1,
            route_name="test.api1",
            request_method="POST",
            request_body_schema={
                "application/json": {"schema": DummySchema()},
                "multipart/form-data": {"schema": DummySchema()},
            },
        )
        request = testing.DummyRequest()
        pyramid.request.apply_request_extensions(request)
        apispec = request.apispec
        assert apispec.to_dict() == {
            "openapi": "3.0.2",
            "info": {
                "title": "test API",
                "version": "0.1+test",
            },
            "paths": {
                "/v1/api1": {
                    "get": {
                        "summary": "get api1 resource",
                        "parameters": [],
                    },
                    "post": {
                        "summary": "create api1 resource",
                        "parameters": [],
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Dummy",
                                    },
                                },
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Dummy",
                                    },
                                },
                            }
                        },
                    },
                },
                "/v1/api2/{id}": {
                    "get": {
                        "summary": None,
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                },
                            }
                        ],
                        "responses": {
                            "default": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/DummyResponse",
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "components": {
                "schemas": {
                    "Dummy": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                            },
                            "value": {
                                "type": "integer",
                            },
                        },
                    },
                    "DummyResponse": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                            },
                            "title": {
                                "type": "string",
                            },
                            "value": {
                                "type": "integer",
                            },
                        },
                    },
                },
            },
        }
