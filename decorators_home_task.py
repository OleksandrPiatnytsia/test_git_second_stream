from functools import wraps
import hashlib

CACHE_RESULTS = {}


def get_cache_key(func, args, kwargs):
    return f"{func.__name__}{"".join([str(a) for a in args])}{"".join([f"{k}{v}" for k, v in kwargs.items()])}"


def get_cache_key_hashlib(func, args, kwargs):
    cache_data = (
        f"{func.__module__}.{func.__qualname__}:{args}:{sorted(kwargs.items())}"
    )
    return hashlib.sha256(cache_data.encode()).hexdigest()


def cache_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # cache_key = get_cache_key(func, args, kwargs)
        cache_key = get_cache_key_hashlib(func, args, kwargs)

        res = CACHE_RESULTS.get(cache_key, None)
        if res:
            print(f"Cache hit: {res}")
            return res

        result = func(*args, **kwargs)
        CACHE_RESULTS.update({cache_key: result})

        return result

    return wrapper


@cache_decorator
def add(a, b):
    print(f"Call {__name__}: {a} * {b} = {a * b}")
    return a + b


@cache_decorator
def mul(a, b):
    print(f"Call {__name__}: {a} * {b} = {a*b}")
    return a * b


@cache_decorator
def square(a):
    print(f"Call {__name__}: {a}**2 = {a ** 2}")
    return a**2


if __name__ == "__main__":
    add(1, 2)
    add(1, 2)
    add(1, 2)
    square(3)
    square(3)
    mul(4, 5)
    mul(4, 5)
    mul(4, 5)
