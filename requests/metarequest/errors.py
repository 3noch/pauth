from pauth.errors import PauthError


class RequestConfigurationError(PauthError):
    pass


class MultipleOAuthParamDefinitionsInParents(RequestConfigurationError)
    def __str__(self):
        return "Two or more of this Request's parents define the same OAuth parameter. Which one is right?"


class MethodMustBeOverriddenByMetaclassError(RequestConfigurationError):
    """
    A trivial error class for exposing the rare case when a class expects one or more of its methods
    to be overridden by its metaclass constructor, but they aren't.
    """
    def __str__(self):
        return 'This method must be overridden by a metaclass!'
