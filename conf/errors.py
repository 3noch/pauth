from pauth.errors import PauthError


class UnconfiguredError(PauthError):
    """
    An error meant to flag the library-user that something is not configured right.
    """
    def __str__(self):
        return ('This Pauth adapter configuration has not been configured yet. '
                'Did you forget to call `pauth.conf.initialize()`?')
