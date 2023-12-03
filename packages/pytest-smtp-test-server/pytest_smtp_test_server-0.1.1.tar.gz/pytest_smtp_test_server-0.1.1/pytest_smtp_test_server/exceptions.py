"""
Package exceptions
"""


class PythonTooOldError(RuntimeError):
    """
    Exception when python version is too old
    """


class PytestTooOldError(RuntimeError):
    """
    Exception when pytest version is too old
    """
