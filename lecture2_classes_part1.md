# Лекція 2. Класи в Python: атрибути, властивості, методи, створення об'єкта

## План

1. Атрибути класу й атрибути екземпляра (і анотації, які їх плутають)
2. Властивості: геттер, сеттер, видалення
3. Три види методів: звичайний, `@classmethod`, `@staticmethod`
4. Інтроспекція: `hasattr`, `getattr`, `setattr`, `delattr`
5. Створення об'єкта: `__new__`, `__init__`, патерн Singleton
6. Міст до магічних методів: `__repr__` і `__str__`

---

## 1. Атрибути класу й атрибути екземпляра

### 1.1 Базове правило

Коли ви пишете `obj.x`, Python шукає `x` у такому порядку: спочатку в самому об'єкті (`obj.__dict__`), потім у його класі, потім у батьківських класах за MRO (пам'ятаєте з першої лекції). Усе, що буде далі, випливає з цього одного правила.

```python
class Student:
    university = "КПІ"

    def __init__(self, name, age):
        self.name = name
        self.age = age


olena = Student("Олена", 19)
ivan = Student("Іван", 20)
print(olena.university, ivan.university, Student.university)
print(olena.__dict__)
print("university" in olena.__dict__)
```

```
КПІ КПІ КПІ
{'name': 'Олена', 'age': 19}
False
```

Зверніть увагу: у `olena.__dict__` немає `university`. Олена не має власної копії, вона лише знаходить значення в класі.

### 1.2 Затінення

А що буде, якщо присвоїти значення через об'єкт?

```python
ivan.university = "ЛНУ"
print(ivan.university, olena.university, Student.university)
print(ivan.__dict__)

Student.university = "КНУ"
print(olena.university, ivan.university)
```

```
ЛНУ КПІ КПІ
{'name': 'Іван', 'age': 20, 'university': 'ЛНУ'}
КНУ ЛНУ
```

Присвоєння `ivan.university = ...` **не змінює клас**. Воно створює новий атрибут саме в Івана, який «затіняє» класовий. Після цього зміна `Student.university` бачить Олена, а Іван уже ні: він має власне значення. Щоб змінити спільне значення для всіх, присвоювати треба через клас.

### 1.3 Анотації полів: три випадки, які плутають

Анотація — це підказка типу в тілі класу: `name: str`. Головне, що треба запам'ятати: **сама по собі анотація атрибута не створює**. Розгляньмо три випадки на роботі:

```python
class Robot:
    model: str
    battery: int = 100

    def __init__(self, name):
        self.name = name


r2 = Robot("R2")
print(Robot.__annotations__)
print(hasattr(r2, "model"))
print(r2.battery, r2.__dict__)
```

```
{'model': <class 'str'>, 'battery': <class 'int'>}
False
100 {'name': 'R2'}
```

| Запис у класі | Що створюється |
| --- | --- |
| `model: str` | Лише запис в `__annotations__`. Атрибута немає: `r2.model` дасть `AttributeError` |
| `battery: int = 100` | Запис в `__annotations__` **і** атрибут класу зі значенням 100 |
| `self.name = name` в `__init__` | Атрибут екземпляра в `r2.__dict__` |

```python
try:
    r2.model
except AttributeError as e:
    print(f"AttributeError: {e}")
```

```
AttributeError: 'Robot' object has no attribute 'model'
```

Звідси типова помилка студентів: вони пишуть `model: str` і думають, що поле існує. Анотація лише документує намір і допомагає редактору та перевіркам типів, але значення вона не створює.

### 1.4 Те саме поле в класі й в `__init__`

Тепер найважливіший для розуміння випадок: поле оголошене в класі зі значенням за замовчуванням, а в `__init__` може бути присвоєне ще раз.

```python
class Pupil:
    age: int = 18

    def __init__(self, name, age=None):
        self.name = name
        if age is not None:
            self.age = age


a = Pupil("Олена")
b = Pupil("Іван", 20)
print(a.age, a.__dict__)
print(b.age, b.__dict__)
print(Pupil.age)
```

```
18 {'name': 'Олена'}
20 {'name': 'Іван', 'age': 20}
18
```

Розберімо по кроках:

- У Олени `age` у `__dict__` немає, тому береться з класу: 18.
- Іван у `__init__` виконав `self.age = age`. Так з'явився **атрибут екземпляра**, який затінив класовий: 20.
- `Pupil.age` усе ще 18. Клас не змінився.

Це одне й те саме ім'я, яке в різних об'єктів «живе» в різних місцях. Перевіряти, де саме, можна через `obj.__dict__` (екземпляр) і `Class.__dict__` (клас).

### 1.5 Пастка: `self.value += 1`

```python
class Counter:
    value: int = 0

    def inc(self):
        self.value += 1


c1, c2 = Counter(), Counter()
c1.inc()
c1.inc()
c2.inc()
print(c1.value, c2.value, Counter.value)
print(c1.__dict__, c2.__dict__)
```

```
2 1 0
{'value': 2} {'value': 1}
```

Студенти очікують спільний лічильник, а отримують три незалежних значення. Причина в тому, що `self.value += 1` розгортається в `self.value = self.value + 1`. Праворуч значення читається з класу, а ліворуч записується в екземпляр. Кожен об'єкт одразу отримує власну копію.

Щоб рахувати спільно, потрібно звертатися до класу:

```python
class Visits:
    total = 0

    def __init__(self):
        Visits.total += 1


Visits()
Visits()
print(Visits.total)
```

```
2
```

### 1.6 Пастка: змінний атрибут класу

Те саме, що ми бачили з `grades=[]` у першій лекції, але тепер на рівні класу:

```python
class BadGroup:
    students = []

    def add(self, name):
        self.students.append(name)


g1, g2 = BadGroup(), BadGroup()
g1.add("Олена")
print(g2.students)
```

```
['Олена']
```

Тут присвоєння немає, є лише `append`, тому нового атрибута екземпляра не з'являється. Обидві групи працюють з одним списком класу. Правильно створювати список в `__init__`:

```python
class GoodGroup:
    def __init__(self):
        self.students = []

    def add(self, name):
        self.students.append(name)


g1, g2 = GoodGroup(), GoodGroup()
g1.add("Олена")
print(g2.students)
```

```
[]
```

Правило: незмінні значення (числа, рядки, кортежі) в атрибутах класу безпечні як значення за замовчуванням. Змінні (списки, словники, множини) створюйте в `__init__`.

### 1.7 `ClassVar` і зв'язок із `@dataclass`

Щоб явно сказати «це атрибут класу, а не поле екземпляра», використовують `ClassVar`:

```python
from typing import ClassVar


class Pupil2:
    university: ClassVar[str] = "КПІ"
    name: str
    age: int
```

Це не просто краса. Модуль `dataclass` будує `__init__` саме за анотаціями, тому йому треба знати, що є полем екземпляра, а що ні:

```python
from dataclasses import dataclass, field


@dataclass
class Point:
    x: float
    y: float = 0.0
    tags: list = field(default_factory=list)


print(Point(1))
print(Point(1, 2, ["a"]))
```

```
Point(x=1, y=0.0, tags=[])
Point(x=1, y=2, tags=['a'])
```

Тут видно відмінність від звичайного класу: у `dataclass` анотація **без** значення (`x: float`) працює як обов'язкове поле, бо `dataclass` читає `__annotations__`. А змінні значення задаються через `field(default_factory=list)`, що вирішує пастку з пункту 1.6.

```python
@dataclass
class Pupil3:
    university: ClassVar[str] = "КПІ"
    name: str
    age: int


p = Pupil3("Олена", 19)
print(p, p.university)
```

```
Pupil3(name='Олена', age=19) КПІ
```

`ClassVar`-поле у конструктор не потрапило, і воно залишилося спільним атрибутом класу.

---

## 2. Властивості: геттер, сеттер, видалення

Властивість (`property`) виглядає зовні як звичайний атрибут, але за читанням і записом стоїть ваш код. Це інструмент інкапсуляції, який ми торкалися в першій лекції. Тепер розберемо його повністю.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Нижче абсолютного нуля")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        print("Видаляю температуру")
        del self._celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32
```

Три декоратори для одного імені:

- `@property` — **геттер**, спрацьовує при читанні `t.celsius`.
- `@celsius.setter` — **сеттер**, спрацьовує при присвоєнні `t.celsius = ...`.
- `@celsius.deleter` — спрацьовує при `del t.celsius`.

Усі три функції мають однакове ім'я. Реальні дані лежать у захищеному полі `_celsius`, а `celsius` — це «фасад».

```python
t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.celsius = 30
print(t.celsius, t.fahrenheit)
```

```
25 77.0
30 86.0
```

Перевірка в сеттері працює і при зміні, і при створенні, бо в `__init__` ми пишемо `self.celsius = celsius`, а не `self._celsius = celsius`:

```python
try:
    t.celsius = -300
except ValueError as e:
    print(f"ValueError: {e}")

try:
    Temperature(-500)
except ValueError as e:
    print(f"ValueError при створенні: {e}")
```

```
ValueError: Нижче абсолютного нуля
ValueError при створенні: Нижче абсолютного нуля
```

### Властивість лише для читання й обчислювана властивість

`fahrenheit` не має сеттера і не має власного поля: значення щоразу обчислюється з `_celsius`. Спроба присвоїти дасть помилку:

```python
try:
    t.fahrenheit = 100
except AttributeError as e:
    print(f"AttributeError: {e}")
```

```
AttributeError: property 'fahrenheit' of 'Temperature' object has no setter
```

### Видалення

```python
del t.celsius
print(hasattr(t, "_celsius"))
```

```
Видаляю температуру
False
```

На практиці deleter потрібен рідко, але без нього набір декораторів неповний, а студенти про нього запитують.

### `cached_property`: обчислити один раз

Якщо властивість важко рахувати, а результат не змінюється, його кешують:

```python
from functools import cached_property


class Report:
    def __init__(self, data):
        self.data = data

    @cached_property
    def total(self):
        print("рахую...")
        return sum(self.data)


rep = Report([1, 2, 3])
print(rep.total)
print(rep.total)
```

```
рахую...
6
6
```

Друге звернення не рахує, а бере збережене значення. Обернена сторона: кеш не знає, що дані змінились.

```python
rep.data.append(100)
print(rep.total)
del rep.total
print(rep.total)
```

```
6
рахую...
106
```

Після `append` значення залишилося старим, а `del rep.total` скидає кеш, і наступне звернення рахує знову. Використовуйте `cached_property` лише там, де вихідні дані не змінюються.

---

## 3. Три види методів

До цього моменту всі наші методи були звичайними: вони отримують `self`, тобто конкретний об'єкт. Але бувають методи, яким об'єкт не потрібен.

```python
class Student2:
    university = "КПІ"
    count = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Student2.count += 1

    @classmethod
    def from_string(cls, text):
        name, age = text.split(",")
        return cls(name.strip(), int(age))

    @classmethod
    def change_university(cls, new_name):
        cls.university = new_name

    @staticmethod
    def is_adult(age):
        return age >= 18

    def info(self):
        return f"{self.name}, {self.age}, {self.university}"
```

### `@classmethod`: працює з класом

Першим параметром отримує не об'єкт, а **сам клас** (за домовленістю `cls`). Два головних застосування:

**1. Альтернативні конструктори.** Створити об'єкт іншим способом, ніж стандартний `__init__`:

```python
s = Student2.from_string("Олена, 19")
print(s.info(), type(s).__name__)
```

```
Олена, 19, КПІ Student2
```

**2. Робота зі станом класу.** Наприклад, змінити спільний атрибут:

```python
Student2.change_university("ЛНУ")
print(s.university)
```

```
ЛНУ
```

Чому в конструкторі `cls(...)`, а не `Student2(...)`? Тому що `cls` — це той клас, від якого викликали метод. Це важливо при наслідуванні:

```python
class Freshman(Student2):
    pass


f = Freshman.from_string("Іван, 17")
print(f.info(), type(f).__name__)
```

```
Іван, 17, КПІ Freshman
```

Метод написано один раз у `Student2`, а повернув він об'єкт саме `Freshman`. Якби всередині було жорстко написано `Student2(...)`, нащадок отримав би об'єкт неправильного типу.

### `@staticmethod`: звичайна функція в просторі імен класу

Не отримує ні `self`, ні `cls`. Це звичайна функція, яку просто покладено в клас, бо вона логічно стосується теми:

```python
print(Student2.is_adult(17), s.is_adult(19))
```

```
False True
```

Викликається і через клас, і через об'єкт, результат однаковий. Якщо методу потрібен стан класу чи об'єкта, він не статичний.

### Як вибрати

| Вид | Перший параметр | Бачить об'єкт | Бачить клас | Для чого |
| --- | --- | --- | --- | --- |
| Звичайний | `self` | так | так (через `self`) | Поведінка конкретного об'єкта |
| `@classmethod` | `cls` | ні | так | Альтернативні конструктори, зміна стану класу |
| `@staticmethod` | немає | ні | ні | Допоміжна функція, логічно пов'язана з класом |

Практичне правило з трьох запитань: чи потрібні дані конкретного об'єкта? Тоді звичайний. Чи потрібен лише клас? Тоді `classmethod`. Не потрібне ні те, ні інше? Тоді `staticmethod` (або взагалі функція поза класом).

---

## 4. Інтроспекція: що є в об'єкта?

Іноді ім'я атрибута відоме лише під час виконання програми, наприклад, воно приходить із файлу чи форми. Для цього є чотири вбудовані функції:

| Функція | Що робить |
| --- | --- |
| `hasattr(obj, "x")` | Чи є атрибут, `True`/`False` |
| `getattr(obj, "x", default)` | Прочитати; якщо немає, повернути `default` (без `default` буде `AttributeError`) |
| `setattr(obj, "x", value)` | Записати, як `obj.x = value` |
| `delattr(obj, "x")` | Видалити, як `del obj.x` |

```python
olena = Student2("Олена", 19)
print(hasattr(olena, "name"), hasattr(olena, "email"))
print(getattr(olena, "email", "немає"))
setattr(olena, "email", "olena@ukr.net")
print(olena.email)
delattr(olena, "email")
print(hasattr(olena, "email"))
```

```
True False
немає
olena@ukr.net
False
```

Типове застосування: обійти кілька полів за іменами.

```python
for field_name in ("name", "age", "email"):
    print(field_name, "->", getattr(olena, field_name, "—"))
```

```
name -> Олена
age -> 19
email -> —
```

Подивитися, що взагалі є в об'єкті:

```python
print(vars(olena))
print([n for n in dir(olena) if not n.startswith("__")])
```

```
{'name': 'Олена', 'age': 19}
['age', 'change_university', 'count', 'from_string', 'info', 'is_adult', 'name', 'university']
```

`vars(obj)` — це `obj.__dict__`, тобто лише власні атрибути екземпляра. `dir(obj)` показує все, що доступне, включно з атрибутами й методами класу.

### Пастка `hasattr`

`hasattr` не просто заглядає в словник. Вона **справді читає атрибут**, тобто виконує геттер властивості, а потім ловить лише `AttributeError`. Звідси три сюрпризи.

**Сюрприз 1: побічні ефекти.**

```python
class Sensor:
    @property
    def value(self):
        print("  (читаю датчик)")
        return 42


print(hasattr(Sensor(), "value"))
```

```
  (читаю датчик)
True
```

Запитали «чи є», а код фактично опитав датчик.

**Сюрприз 2: інші винятки не ловляться.**

```python
class BrokenSensor:
    @property
    def value(self):
        raise RuntimeError("датчик відключено")


try:
    hasattr(BrokenSensor(), "value")
except RuntimeError as e:
    print(f"RuntimeError: {e}")
```

```
RuntimeError: датчик відключено
```

**Сюрприз 3: помилка всередині геттера маскується під «атрибута немає».**

```python
class Sneaky:
    @property
    def value(self):
        return self.missing_field


print(hasattr(Sneaky(), "value"))
```

```
False
```

Властивість `value` у класі є, але всередині неї звернулися до неіснуючого поля, і `hasattr` чесно відповіла `False`. Знайти таку помилку складно.

Якщо потрібно перевірити наявність, не запускаючи код, є `inspect.getattr_static`, який повертає сам об'єкт властивості, не викликаючи його:

```python
import inspect

print(inspect.getattr_static(Sensor(), "value", "немає"))
```

```
<property object at 0x7f7301dbede0>
```

(адреса в кожному запуску своя).

---

## 5. Створення об'єкта: `__new__` і `__init__`

Ми звикли думати, що `__init__` створює об'єкт. Насправді створення — це два кроки:

1. **`__new__(cls, ...)`** — створює порожній об'єкт і повертає його. Це статичний метод, який отримує клас.
2. **`__init__(self, ...)`** — отримує вже створений об'єкт і заповнює його даними.

```python
class Demo:
    def __new__(cls, *args):
        print("__new__: створюю")
        return super().__new__(cls)

    def __init__(self, name):
        print("__init__: заповнюю")
        self.name = name


Demo("тест")
```

```
__new__: створюю
__init__: заповнюю
```

Перевизначати `__new__` потрібно рідко. Найвідоміший випадок — патерн Singleton.

### Singleton: клас з єдиним об'єктом

Іноді об'єкт має бути лише один на всю програму: конфігурація, пул з'єднань. Ідея проста: `__new__` створює об'єкт лише вперше, а далі повертає той самий.

Наївна реалізація:

```python
class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, env="dev"):
        print(f"__init__ з env={env}")
        self.env = env


a = Config("prod")
b = Config("test")
print(a is b, a.env, b.env)
```

```
__init__ з env=prod
__init__ з env=test
True test test
```

Об'єкт один (`a is b` дає `True`), але є пастка. Python **викликає `__init__` після кожного `Config(...)`**, навіть якщо `__new__` повернув уже наявний об'єкт. Тому друге створення затерло `"prod"` значенням `"test"`. Для конфігурації це небезпечна поведінка.

Виправлення: ініціалізувати дані лише при першому створенні, а `__init__` не писати взагалі:

```python
class Settings:
    _instance = None

    def __new__(cls, env="dev"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.env = env
        return cls._instance


a = Settings("prod")
b = Settings("test")
print(a is b, a.env, b.env)
```

```
True prod prod
```

Що варто сказати студентам про Singleton:

- Модуль у Python уже є природним синглтоном: його код виконується один раз, і всі отримують той самий об'єкт. Часто достатньо створити об'єкт на рівні модуля й імпортувати його.
- Патерн вважають спірним, бо це по суті глобальний стан: код стає прихованим чином залежним від нього, а тести ускладнюються.
- Наведена реалізація не потокобезпечна. Для багатопотокових програм потрібне блокування, але це окрема тема.

---

## 6. Міст до магічних методів: `__repr__` і `__str__`

Усі методи з подвійним підкресленням (`__init__`, `__new__`, `__eq__`) називають **магічними** (dunder-методами, від *double underscore*). Ви їх не викликаєте напряму: їх викликає Python у відповідь на певні дії. `__init__` спрацьовує при `Student(...)`, і саме так працюватимуть усі інші.

Почнімо з найпростішого питання: що буде, якщо вивести об'єкт?

```python
class Plain:
    pass


print(repr(Plain())[:22] + "...")
```

```
<__main__.Plain object...
```

Далі йде адреса в пам'яті, яка нічого не каже про вміст. Виправляють це двома магічними методами:

```python
class Student3:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Student3({self.name!r}, {self.age})"

    def __str__(self):
        return f"{self.name}, {self.age} р."


s = Student3("Олена", 19)
print(s)
print(repr(s))
print([s])
print(f"{s}", f"{s!r}")
```

```
Олена, 19 р.
Student3('Олена', 19)
[Student3('Олена', 19)]
Олена, 19 р. Student3('Олена', 19)
```

| Метод | Для кого | Коли викликається | Приклад |
| --- | --- | --- | --- |
| `__str__` | Для людини | `print(obj)`, `str(obj)`, `f"{obj}"` | `Олена, 19 р.` |
| `__repr__` | Для розробника | `repr(obj)`, виведення в списках, консоль, налагодження | `Student3('Олена', 19)` |

Правило: `__repr__` має бути однозначним і, по можливості, виглядати як код, яким об'єкт створюється. Зверніть увагу, що в списку Python використав саме `__repr__`, а не `__str__`. Якщо визначити лише `__repr__`, то `print(obj)` теж скористається ним. Тому мінімум для будь-якого класу — `__repr__`.

Наступна лекція буде присвячена іншим магічним методам: порівнянню, арифметиці, `len`, `in`, ітерації та іншим.

---

## Підсумок

- Пошук `obj.x`: спочатку екземпляр, потім клас, потім батьки. Присвоєння `obj.x = ...` завжди пише в екземпляр і затіняє класовий атрибут.
- Анотація `x: int` без значення атрибута не створює. Зі значенням створює атрибут класу.
- `self.x += 1` читає з класу, а пише в екземпляр. Для спільного лічильника звертайтеся до класу.
- Змінні значення за замовчуванням створюйте в `__init__` (або через `field(default_factory=...)` у `dataclass`).
- `@property` + `@x.setter` + `@x.deleter` — повний набір для керованого доступу. Обчислювані властивості не мають власного поля.
- `@classmethod` отримує клас (альтернативні конструктори, стан класу). `@staticmethod` не отримує нічого.
- `hasattr` викликає геттер і ловить лише `AttributeError`.
- Створення об'єкта: `__new__` створює, `__init__` заповнює, і `__init__` викликається при кожному виклику класу.
- Мінімум для кожного класу: `__repr__`.

## Типові помилки студентів

1. Вважають, що `name: str` у класі створює поле.
2. Очікують спільного лічильника від `self.count += 1`.
3. Кладуть список чи словник в атрибут класу.
4. Пишуть у `__init__` `self._x = x` замість `self.x = x`, і перевірка в сеттері не спрацьовує при створенні.
5. Використовують `hasattr` для властивостей з побічними ефектами.
6. Жорстко пишуть назву класу замість `cls` у `classmethod`.
7. Забувають, що `__init__` Singleton-класу викликається щоразу.

## Питання для самоперевірки

1. Чим відрізняється `model: str` від `model: str = "X"` у тілі класу? Що покаже `hasattr(obj, "model")` в обох випадках?
2. Чому `ivan.university = "ЛНУ"` не змінює значення для Олени? Де це значення тепер зберігається?
3. Що виведе `c1.value, c2.value, Counter.value` після двох викликів `c1.inc()` і одного `c2.inc()`, і чому?
4. Чому в `from_string` пишуть `cls(...)`, а не `Student2(...)`?
5. Коли `staticmethod` краще винести з класу в звичайну функцію?
6. Назвіть три сюрпризи `hasattr` для властивостей.
7. Чому в наївному Singleton `a.env` перетворюється на `"test"`? Як це виправити?
8. Чим `__str__` відрізняється від `__repr__`? Що з них використовується при виведенні списку об'єктів?
