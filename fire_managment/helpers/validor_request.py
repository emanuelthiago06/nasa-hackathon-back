import pydantic
from functools import wraps
from rest_framework.exceptions import APIException, ValidationError
from fire_managment.helpers.deserializer import Deserializer


class RequestValidator(Deserializer):

    def __init__(self, request, kwargs=None):
        super(RequestValidator, self).__init__(
            request=request,
            kwargs=kwargs
        )

    def validate_request(self, model) -> None:
        try:
            if model:
                RequestValidator.deserialize(self=self, model=model)
            pass
        except Exception as validation_error:
            raise ValidationError(detail={
                "status": "error",
                "message": "Invalid request parameters.",
                "error_messages": validation_error.errors()
            })


def validate_request(model=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            request_validator = RequestValidator(request=request, kwargs=kwargs)
            request_validator.validate_request(model=model)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
