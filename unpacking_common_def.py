
def base_zip_def():
    names = ["Oleksandr", "Ivan", "Anna"]
    scores = [85, 92, 78]

    for name, score in zip(names, scores):
        print(f"{name}: {score}")


def list_zip_def():
    names = ["Oleksandr", "Ivan", "Anna"]
    ages = [37, 25, 30]
    # sur_names = ["One", "Two", "Three"]

    zip_res = zip(names, ages)
    print(type(zip_res))
    users = list(zip_res)

    print(users)
    # [('Oleksandr', 37), ('Ivan', 25), ('Anna', 30)]

def swap():
    a = 1
    b = 2

    print(f"a = {a}, b = {b}")

    a,b = b,a

    print(f"a = {a}, b={b}")



def dict_zip_def():
    keys = ["name", "age", "city", "zip_code"]
    values = ["Oleksandr", 37, "Kyiv"]

    user = dict(zip(keys, values))

    print(user)
    # {'name': 'Oleksandr', 'age': 37, 'city': 'Kyiv'}


def base_unpacking_def():
    # user = ["Oleksandr", 37, "Kyiv"]
    #
    # name, age, city = user
    #
    # print(name)
    # print(age)
    # print(city)

    num_dict = {i:str(i) for i in range(10)}

    # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    f, sadasd, *last = num_dict

    print(f)  # [2, 3, 4]
    print(sadasd)  # 1
    print(last)  # 5


def unpacking_func_def():
    def calculate(a, b, c):
        return a + b + c

    numbers = [10, 20, 30]

    result = calculate(*numbers)

    print(result)
    # 60


def unpacking_func_kv_def():
    def create_user(name, age, city):
        return f"{name}, {age}, {city}"

    user = {
        "name": "Oleksandr",
        "age": 37,
        "city": "Kyiv",
    }

    print(create_user(**user))


def unpacking_func_args_def():
    def calculate_sum(*args):
        print(type(args))
        print(args)

        a,b,c = args
        print(type(c))

        return a+b

    print(calculate_sum(1, 2, 3))
    print(calculate_sum(10, 20, 30, 40))


def unpacking_func_kwargs_def():
    def create_user(**kwargs):
        print(kwargs)
        print(type(kwargs))

    create_user(
        name="Oleksandr",
        age=37,
        city="Kyiv",
    )


def unpacking_func_args_kwargs_def():
    def debug_function(*args, **kwargs):
        print("args:", args)
        print("kwargs:", kwargs)

    debug_function(
        10,
        20,
        30,
        40,
        name="Oleksandr",
        city="Kyiv",
    )


def square(x):
    return x**2


def lambda_def():

    _square = lambda x, y: x**2+y
    print(_square(5))
    # 25

    print(_square(5))
    # 25


def map_lambda_def():

    numbers = [1, 2, 3, 4, 5]
    # squares = []
    # for number in numbers:
    #     sq_res = square(number)
    #     squares.append(sq_res)
    # print(squares)

    squares = map(lambda x: x ** 2, numbers)
    #
    # print(list(squares))
    # # [1, 4, 9, 16, 25]
    #
    squares = map(square, numbers)
    print(list(squares))
    # # [1, 4, 9, 16, 25]


def map_two_collections_def():
    prices = [100, 200, 300]
    discounts = [10, 20, 30]

    result = map(
        lambda price, discount: price - discount,
        prices,
        discounts,
    )

    print(list(result))
    # [90, 180, 270]


def zip_map_lambda_def():
    prices = [100, 200, 300]
    quantities = [2, 3, 4]

    totals = map(
        lambda item: item[0] * item[1],
        zip(prices, quantities),
    )

    print(list(totals))
    # [200, 600, 1200]

    # totals = map(
    #     lambda price, quantity: price * quantity,
    #     prices,
    #     quantities,
    # )


def filter_def():
    numbers = [1, 2, 3, 4, 5, 6]

    even_numbers = filter(
        lambda x: x % 2 == 0,
        numbers,
    )
    print(type(even_numbers))
    for i in even_numbers:
        print(i)

    print(list(even_numbers))
    # [2, 4, 6]


def sorted_def():
    users = [
        {"name": "Anna", "age": 30},
        {"name": "Ivan", "age": 20},
        {"name": "Oleksandr", "age": 37},
    ]

    users = sorted(
        users,
        key=lambda user: user["age"],
        reverse=True,
    )

    print(users)


def kwargs_unpacking():
    default_config = {
        "host": "localhost",
        "port": 8000,
    }

    custom_config = {
        "port": 9000,
        "debug": True,
    }

    config = {
        **default_config,
        **custom_config,
    }

    print(config)


def enumerate_def():
    users = ["Anna", "Ivan", "Oleksandr"]

    for index, user in enumerate(users, start=1):
        print(index, user)


def any_all_def():
    numbers = [2, 4, 6, 8]

    print(all(x % 2 == 0 for x in numbers))
    # True

    print(any(x > 10 for x in numbers))
    # False


def finally_def():
    users = [
        {"name": "Anna", "age": 25, "salary": 30000},
        {"name": "Ivan", "age": 35, "salary": 45000},
        {"name": "Oleksandr", "age": 38, "salary": 50000},
    ]

    names = map(
        lambda user: user["name"],
        filter(
            lambda user: user["age"] >= 30,
            users,
        ),
    )

    print(list(names))
    # ['Ivan', 'Oleksandr']


if __name__ == "__main__":
    finally_def()

