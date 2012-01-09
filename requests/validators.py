from functools import wraps

import errors


def validates_request(func):
    """
    Decorates request validator functions by turning them into higher-order
    functions. The higher-order function takes parameters that get "compiled"
    into the resulting function. The resulting function only takes a request
    that needs to be validated. This allows requests to create their own
    custom validators.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        def validate(request):
            func(request, *args, **kwargs)
        return validate
    return wrapper


@validates_request
def has_method(request, allowed_methods):
    """
    Raises an error if the given request's method is not allowed.
    """
    if not request.method in allowed_methods:
        raise errors.InvalidAuthorizationRequestError(request)


@validates_request
def has_parameters(request, parameters):
    """
    Raises an error if the given request doesn't have all of its required parameters.
    """
    if not all(r in request.parameters for r in parameters):
        raise errors.InvalidAuthorizationRequestError(request)


@validates_request
def has_response_type(request, response_type):
    if request.response_type != response_type:
        raise errors.UnsupportedResponseTypeError(request)


@validates_request
def has_grant_type(request, grant_type):
    if request.grant_type != grant_type:
        raise errors.UnsupportedGrantTypeError(request)
