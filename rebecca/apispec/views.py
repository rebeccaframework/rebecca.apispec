import logging

from marshmallow.exceptions import ValidationError
from pyramid.view import view_config

logger = logging.getLogger(__name__)


@view_config(route_name="apispec.swagger-json", renderer="json")
def swagger(request):
    return request.apispec.to_dict()


@view_config(renderer="json", context=ValidationError)
def validation_error(context, request):
    logger.debug(context)
    request.response.status = 400
    return {"errors": context.messages}
