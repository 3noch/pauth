from pauth.requests import errors, parameters as params, Request


class MockRequest(object):
    def __init__(self):
        self.parameters = {}


class MockParameter(params.RequestParameter):
    NAME = 'mock_parameter'


def check_get_from_request(request, parameter, param_name):
    request.parameters['mock_parameter'] = "mock parameter's value"
    assert parameter.get_from_request(request) == "mock parameter's value"
