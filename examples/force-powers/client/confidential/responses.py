from django.template.response import TemplateResponse


class NoCodeResponse(TemplateResponse):
    def __init__(self, request):
        super(NoCodeResponse, self).__init__(request, 'error.html', {'error': 'no_code_provided'})
