## 🧩 1. Практична задача

### Перепишіть код у простій формі, без використання:
- comprehension;
- lambda-функцій;
- `map()`;
- `filter()`;
- `zip()`.

```python
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
```

### Очікуваний результат

```text
['Ivan', 'Oleksandr']
```

---

## 🧩 2. Практична задача

Є список товарів:

```python
products = [
    {"name": "Laptop", "price": 45000, "stock": 5},
    {"name": "Phone", "price": 25000, "stock": 0},
    {"name": "Monitor", "price": 12000, "stock": 10},
    {"name": "Keyboard", "price": 3000, "stock": 20},
]
```

Необхідно:

1. Відібрати тільки товари, які є в наявності (`stock > 0`) за допомогою `filter()`.
2. За допомогою `map()` отримати окремо:
   - назви товарів;
   - ціни товарів.
3. За допомогою `zip()` об'єднати назви та ціни.
4. У циклі використати **unpacking**, щоб отримати `name` і `price`.
5. Вивести назву та ціну кожного доступного товару у форматі:

### Очікуваний результат

```text
Laptop: 45000 грн
Monitor: 12000 грн
Keyboard: 3000 грн
```