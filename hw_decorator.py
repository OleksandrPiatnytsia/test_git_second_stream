import hashlib
from functools import wraps

CACHE_DICT = {}

def get_cache_key_hashlib(func, args, kwargs):
    cache_data = (
        f"{func.__module__}.{func.__qualname__}:{args}:{sorted(kwargs.items())}"
    )
    return hashlib.sha256(cache_data.encode()).hexdigest()

def cache_result(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        cache_key = f"{func.__name__}{"".join([str(a) for a in args])}{"".join([f"{k}{v}" for k,v in kwargs.items()])}"

        # cache_key = get_cache_key_hashlib(func, args, kwargs)

        print(f"Cache key: {cache_key}")

        res = CACHE_DICT.get(cache_key, None)
        if res:
            print(f"Cache hit: {func.__name__}: {args},  {kwargs}")
            return res

        result = func(*args, **kwargs)

        CACHE_DICT.update({cache_key: result})

        return result

    return wrapper


@cache_result
def add(a, b):
    print(f"Call add: {a} * {b} = {a * b}")
    return a + b


@cache_result
def mul(a, b):
    print(f"Call mul: {a} * {b} = {a*b}")
    return a * b


@cache_result
def square(a):
    print(f"Call square: {a}**2 = {a ** 2}")
    return a**2

if __name__ == '__main__':
    add(1, 2)
    add(1, 2)
    add(b = 2, a = 1)
    add(b=2, a = 1)
    add(a = 1, b = 2)
    # square(2)
    # square(2)
    # square(2)
    # mul(2, 4)
    # mul(2, 4)
    # mul(2, 4)
