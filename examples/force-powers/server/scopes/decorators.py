from responses import JsonResponse


def scopes_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        scopes = view_func(request, *args, **kwargs)
        scopes_data = {scope.id: scope.description for scope in scopes}
        return JsonResponse(scopes_data)

    return wrapper
