from pauth.conf import _unconfigured
from errors import UnconfiguredError


def test_unconfigured():
    try:
        _unconfigured()
    except UnconfiguredError:
        pass
