import urllib.parse

import marshmallow


class SchemaRenderer:
    def __init__(self, info):
        pass

    def get_response_def(self, schemas, status_code):
        for k, v in schemas.items():
            if status_code == k:
                return v
        return schemas["default"]

    def __call__(self, value, system):
        request = system["request"]
        schemas = request.apispec_schemas
        response_schemas = schemas["response_schemas"]
        status_code = str(request.response.status_int)
        content_type = request.response.content_type
        response_def = self.get_response_def(response_schemas, status_code)
        schema = response_def["content"][content_type]["schema"]
        if content_type == "application/json":
            body = schema.dumps(value)
        elif content_type == "application/x-www-form-urlencoded":
            body = urllib.parse.urlencode(
                schema.load(value, unknown=marshmallow.EXCLUDE),
            )
        return body
