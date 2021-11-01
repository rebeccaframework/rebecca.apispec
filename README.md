# rebecca.apispec

An apispec extension for pyramid web framework.

## Get Started

```
pip install rebecca.apispec
```

```
config.include("rebecca.apispec")
```

## directives

### add_apispec

`add_apispec` is directive to add apispec global information.

```
config.add_apispec(title="example API", version="0.1")
```

### get_apispec

```
apispec = config.get_apispec()
```

## request method

### apispec

`apispec` is property for apispec.

```
apispec = request.apispec
request.apispec.to_dict()
```

## view predicates

### request_body_schema

```
add_view(
   ...
   responses_schema=DummyResponseSchema(),
)
```

```
add_view(
   ...
   request_body_schema={
       "application/json": {"schema": DummySchema()},
       "multipart/form-data": {"schema": DummySchema()},
   },
)
```

### query_schema

```
add_view(
   query_schema=DummyQuerySchema(),
)
```

### responses_schema

```
add_view(
   responses_schema=responses_schema=DummyResponseSchema(),
)
```

```
add_view(
   responses_schema={
     "200": {
         "content": {
             "application/json": {"schema": responses_schema=DummyResponseSchema()}
         }
     }
)
```

## view renderers

### apispec-schema

render body from dumps of `responses_schema`.

```
add_view(
   responses_schema=responses_schema=DummyResponseSchema(),
   renderer="apispec-schema",
)
```

## swagger tools

### swagger ui

`rebecca.apispec` bundles swagger ui and hosts on `/apispec.swaggerui`.

### redoc

`rebecca.apispec` hosts on `/apispec.redoc`.
