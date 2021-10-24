import marshmallow


class UploadSchema(marshmallow.Schema):
    data = marshmallow.fields.Raw(
        metadata={
            "type": "string",
            "format": "binary",
        },
    )


class DocumentSearchSchema(marshmallow.Schema):
    keyword = marshmallow.fields.List(marshmallow.fields.String())
    q = marshmallow.fields.String()


class DocumentSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer()
    title = marshmallow.fields.String()
    contents = marshmallow.fields.String()
    tags = marshmallow.fields.List(marshmallow.fields.String())


class DocumentListSchema(marshmallow.Schema):
    items = marshmallow.fields.Nested(DocumentSchema, many=True)
