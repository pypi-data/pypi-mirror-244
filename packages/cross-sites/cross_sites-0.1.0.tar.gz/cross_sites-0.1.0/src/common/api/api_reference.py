# TODO APIReferSchema
# TODO Document by decorator
# TODO
import inspect
from functools import wraps


# OUTCOME: yaml, json reference files


class APIReference:
    def __init__(self):
        self._refer = {}

    def refer(self, *arg, **kwargs):
        path = kwargs.get("path", "")
        methods = kwargs.get("methods", [])
        registered_handlers = []
        prefix = "/"
        if not registered_handlers:
            registered_handlers = []

        def decorator(func):
            if not callable(func):
                raise RuntimeError(f"{func} is not callable")
            module = inspect.getmodule(func).__name__
            self._refer.update(
                {
                    f"{path}": {
                        "handler": f"{module}.{func.__name__}",
                        "methods": methods,
                        "prefix": prefix if prefix else "",
                        "registeredHandlers": registered_handlers
                        if registered_handlers
                        else [],
                    },
                }
            )
            return func

        return decorator
