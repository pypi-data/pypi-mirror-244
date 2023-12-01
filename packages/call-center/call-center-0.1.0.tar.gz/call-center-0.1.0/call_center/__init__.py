try:
    from ._version import __version__
except ModuleNotFoundError:
    import warnings

    warnings.warn("call-center was not properly installed!")
    del warnings

    __version__ = "UNKNOWN"

from ._agent import Agent
