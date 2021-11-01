class RequestBodySchemaPredicate:
    def __init__(self, value, info):
        self.value = value
        if isinstance(value, dict):
            self.content = value
        else:
            self.content = {"application/json": {"schema": value}}

    def phash(self):
        return ",".join([f"{k}:{s}" for k, s in self.content.items()])

    text = phash

    def find_content(self, request_content_type):
        for content_type, content in self.content.items():
            if content_type == request_content_type.split(";", 1)[0]:
                return content_type, content
        return None

    def __call__(self, context, request):
        found = self.find_content(request.content_type)
        if not found:
            return False
        content_type, content = found
        if content_type == "application/json":
            body = request.json
        elif content_type in (
            "multipart/form-data",
            "application/x-www-form-urlencoded",
        ):
            body = request.params
        else:
            body = request.body
        request.data = content["schema"].load(body)
        return True


class QuerySchemaPredicate:
    def __init__(self, value, info):
        self.schema = value

    def phash(self):
        return str(self.schema)

    text = phash

    def __call__(self, context, request):
        request.query_data = self.schema.load(request.GET)
        return True


class ResponsesSchemaPredicate:
    def __init__(self, value, info):
        self.value = value
        if isinstance(value, dict):
            self.content = value
        else:
            self.content = {
                "default": {
                    "content": {
                        "application/json": {"schema": value},
                    },
                },
            }

    def phash(self):
        return ",".join([f"{k}:{s}" for k, s in self.content.items()])

    text = phash

    def __call__(self, context, request):
        apispec_schemas = {}
        if hasattr(request, "apispec_schemas"):
            apispec_schemas.update(request.apispec_schemas)
        apispec_schemas["response_schemas"] = self.content
        request.apispec_schemas = apispec_schemas
        return True
