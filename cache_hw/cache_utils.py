from datetime import datetime

from pymemcache.client import base

client = base.Client(('127.0.0.1', 11211))


def data_converter(data, convert_to):
    if isinstance(data, bytes):
        if convert_to == str:
            return data.decode('utf-8')
        elif convert_to == int:
            return int(data)
    else:
        return str(data)


def cache_result(func):
    def wrapper(n):
        result = client.get(str(n))
        if result is None:
            result = func(n)
            client.set(str(n), int(result))
        return int(result)

    return wrapper


def cache_update(func):
    def wrapper(*args, **kwargs):
        n = args[0]
        value = kwargs.get('value')
        result = client.get(str(n))
        if result is None:
            result = func(n)
            client.set(str(n), result)
        elif value and value != result:
            result = func(n, value)
            client.set(str(n), value)
        return result
    return wrapper


@cache_result
def fibonacci(n):
    if int(n) <= 2:
        return 1
    return fibonacci(int(n) - 1) + fibonacci(int(n) - 2)
