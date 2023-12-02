from functools import wraps


class GeneralException(Exception):
    def __init__(self, code, msg=""):
        self.code = code
        self.msg = msg

    def __eq__(self, other):
        return self.code == other.code


_exceptions = {}


def exception_handle(exceptions: [Exception], handler):
    for ex in _exceptions:
        _exceptions.update({ex: handler})

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except tuple(exceptions) as ex:
                return handler(ex)

        return inner

    return decorator


def get_exceptions():
    return list(_exceptions.keys())
