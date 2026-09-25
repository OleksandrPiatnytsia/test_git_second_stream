"""
Python lecture examples:
- First-class objects
- Functions as values
- Functions as arguments
- Functions returning functions
- Nested functions
- Closures
- Decorators
- Decorators with arguments
- functools.wraps
- Multiple decorators
- FastAPI decorator analogy

Run:
    python first_class_objects_and_decorators.py
"""



# ============================================================
# 1. CLOSURE
# ============================================================

def create_greeting(name):

    def greeting():
        print(f"Hello, {name}!")

    return greeting


# if __name__ == '__main__':
#
#     hello_alex = create_greeting("Alex")
#     hello_ivan = create_greeting("Ivan")
#
#     print(hello_alex.__name__)
#     print(hello_ivan.__name__)
#
#     hello_alex()
#     hello_ivan()


# ============================================================
# 2. FIRST-CLASS OBJECTS/COTIZENS
# ============================================================

def hello():
    print("Hello!")

# foo = hello

# print(foo.__name__)
# foo()



# ============================================================
# 3. FUNCTION AS AN ARGUMENT
# ============================================================



def execute(func):
    func()


# execute(hello)


# ============================================================
# 4. FUNCTION RETURNING ANOTHER FUNCTION
# ============================================================

def create_function():

    def hello():
        print("Hello from inner function!")

    hello()

    return hello


# my_function = create_function()
# my_function()

# ============================================================
# 5. NESTED FUNCTIONS
# ============================================================

def outer():

    def inner():
        print("Inside inner function")

    inner()


# outer()
# `inner()` exists inside `outer()`.


# ============================================================
# 6. SIMPLE DECORATOR
# ============================================================

def decorator(func):

    def wrapper():
        print("Before")

        func()

        print("After")

    return wrapper


def decorated_hello():
    print("Hello!")


# decorated_hello = decorator(decorated_hello)

# decorated_hello()


# After:
#
# decorated_hello
#       |
#       v
#     wrapper
#       |
#       v
# original decorated_hello
#
#
# This:
#
#     decorated_hello = decorator(decorated_hello)
#
# can be written using @ syntax.


# ============================================================
# 7. @ DECORATOR SYNTAX
# ============================================================

def simple_decorator(func):

    def wrapper():
        print("Before function")

        func()

        print("After function")

    return wrapper


@simple_decorator
def say_something():
    print("Something!")


# say_something()


# This:
#
# @simple_decorator
# def say_something():
#     ...
#
# is equivalent to:
#
# def say_something():
#     ...
#
# say_something = simple_decorator(say_something)


# ============================================================
# 8. REALISTIC LOGGING DECORATOR
# ============================================================


def log_function(func):

    def wrapper():
        print(f"Calling {func.__name__}")

        result = func()

        print(f"Finished {func.__name__}")

        return result

    return wrapper


@log_function
def get_user():
    print("Getting user")


@log_function
def get_products():
    print("Getting products")


# get_user()
# get_products()


# ============================================================
# 9. DECORATOR WITH *args AND **kwargs
# ============================================================


def log_function_with_args(func):

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Finished {func.__name__}")

        return result

    return wrapper


@log_function_with_args
def hello_user(name):
    print(f"Hello, {name}!")


@log_function_with_args
def add(a, b):
    print(f"a = {a} b = {b}")
    return a + b

# add(b=20, a=10)

# hello_user("Alex")
#
# result = add(10, 20)
#
# print(f"Result: {result}")


# `*args` collects positional arguments.
# `**kwargs` collects keyword arguments.
#
# This makes the decorator compatible with almost any function.


# ============================================================
# 10. functools.wraps
# ============================================================

from functools import wraps

def log_with_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Finished {func.__name__}")

        return result

    return wrapper


@log_with_wraps
def multiply(a, b):
    """Multiply two numbers."""
    return a * b


# result = multiply(5, 6)
#
# print(f"Result: {result}")
# print(f"Function name: {multiply.__name__}")
# print(f"Docstring: {multiply.__doc__}")


# Without @wraps:
#
# multiply.__name__
#
# could be:
#
# "wrapper"
#
# With @wraps(func):
#
# multiply.__name__
#
# remains:
#
# "multiply"


# ============================================================
# 11. DECORATOR WITH PARAMETERS
# ============================================================

def retry(attempts):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)

                except Exception:
                    if attempt == attempts - 1:
                        raise

                    print(
                        f"Attempt {attempt + 1} failed. "
                        f"Retrying..."
                    )

        return wrapper

    return decorator


@retry(3)
def get_data():
    print("Executing get_data()")

    raise RuntimeError("Something went wrong")


# try:
#     get_data()
# except RuntimeError:
#     print("All attempts failed")


# Important:
#
# @retry(3)
# def get_data():
#     ...
#
# is equivalent to:
#
# get_data = retry(3)(get_data)
#
#
# There are three levels:
#
# retry(3)
#     |
#     v
# decorator
#     |
#     v
# wrapper
#     |
#     v
# original function


# ============================================================
# 12. MULTIPLE DECORATORS
# ============================================================

def decorator_a(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator A - before")

        result = func(*args, **kwargs)

        print("Decorator A - after")

        return result

    return wrapper


def decorator_b(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator B - before")

        result = func(*args, **kwargs)

        print("Decorator B - after")

        return result

    return wrapper


@decorator_a
@decorator_b
def hello_multiple():
    print("Hello!")


hello_multiple()


# ============================================================
# 13. UNIVERSAL TIMING DECORATOR
# ============================================================

import time

def measure_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} started")

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        print(
            f"{func.__name__} finished "
            f"in {elapsed:.6f} seconds"
        )

        return result

    return wrapper


@measure_time
def calculate():
    total = 0

    for number in range(1_000_000):
        total += number

    return total


# result = calculate()
#
# print(f"Result: {result}")


# ============================================================
# 15. COMPLETE MENTAL MODEL
# ============================================================

# print(
#     """
# Functions are objects
#         |
#         v
# Functions can be assigned to variables
#         |
#         v
# Functions can be passed as arguments
#         |
#         v
# Functions can return functions
#         |
#         v
# Nested functions
#         |
#         v
# Closures
#         |
#         v
# Decorators
#         |
#         v
# @decorator
#         |
#         v
# Decorator with parameters
# """
# )


# ============================================================
# 16. FINAL EXAMPLE
# ============================================================


def log_call(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")

        result = func(*args, **kwargs)

        print(f"[LOG] {func.__name__} returned {result}")

        return result

    return wrapper


def retry_on_error(attempts):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)

                except Exception as exc:
                    print(
                        f"[RETRY] Attempt "
                        f"{attempt + 1} failed: {exc}"
                    )

                    if attempt == attempts - 1:
                        raise

        return wrapper

    return decorator


@log_call
@retry_on_error(3)
def divide(a, b):
    return a / b

# result = divide(10, 2)
#
# print(f"Final result: {result}")

# The final structure is approximately:
#
# divide
#   |
#   v
# log_call wrapper
#   |
#   v
# retry_on_error wrapper
#   |
#   v
# original divide function
#
#
# This is the fundamental mechanism behind many
# Python frameworks and libraries.



