from pauth.requests import errors, parameters as params, Request


class MockRequest(object):
    def __init__(self):
        self.query_args = {}


class MockParameter(params.RequestParameter):
    NAME = 'mock_parameter'


def check_get_from_request(request, parameter, param_name):
    request.query_args['mock_parameter'] = "mock parameter's value"
    assert parameter.get_from_request(request) == "mock parameter's value"
