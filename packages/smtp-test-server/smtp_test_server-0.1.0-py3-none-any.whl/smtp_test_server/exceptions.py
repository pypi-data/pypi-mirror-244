"""
Package exceptions
"""


class AlreadyStartedError(RuntimeError):
    """
    Exception when the server is already running
    """


class NotStartedError(RuntimeError):
    """
    Exception when the server is not started
    """


class NotALocalHostnameOrIPAddressToBindToError(ValueError):
    """
    Exception when the hostname is not local
    """


class NotProperlyInitializedError(RuntimeError):
    """
    Exception when not properly initialized
    """
