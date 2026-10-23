# ======================================================================
#  ООП: Інкапсуляція, Наслідування, Поліморфізм, Абстракція
# ======================================================================

from abc import ABC, abstractmethod

# ======================================================================
# КЛАС І ОБ'ЄКТ
# ======================================================================


class Student:
    university = "КПІ"
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Я студент {self.name}, мені {self.age}, навчаюсь у {self.university}"


olena_1 = Student("Олена", 19)
olena_2 = Student("Олена", 19)

ivan = Student("Іван", 20)

# ======================================================================
# 1. ІНКАПСУЛЯЦІЯ
# ======================================================================


class BankAccount:
    def __init__(self, owner, balance=0, pin="0000"):
        self.owner = owner
        self._balance = balance
        self.__pin = pin

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сума має бути додатною")
        self._balance += amount

    def withdraw(self, amount, pin):
        if pin != self.__pin:
            raise PermissionError("Невірний PIN")
        if amount > self._balance:
            raise ValueError("Недостатньо коштів")
        self._balance -= amount


acc = BankAccount("Іван", 999)
# print(acc.__pin)

# acc.deposit(50)
acc.withdraw(30, "0000")
print(acc.balance)
#
#

# print(acc.balance)


# class Robot(Participant):
#     def __init__(self, name):
#         self.name = name
#         self.__battery = 100
#         self.__battery_usage_per_hour = 10
#
#     @property
#     def battery(self):
#         return self.__battery
#
#     def charge(self, percent):
#         self.__battery = min(100, self.__battery + percent)
#
#     def work(self, hours):
#         needed = hours * self.__battery_usage_per_hour
#         if needed > self.__battery:
#             raise RuntimeError("Недостатньо заряду")
#         self.__battery -= needed
#
#     def introduce(self):
#         return f"Я робот {self.name}, готовий до роботи"

# r2d2 = Robot("r2d2")
# r2d2.work(3)
# print(r2d2.battery)
# r2d2.charge(50)
# print(r2d2.battery)
# try:
#     r2d2.work(20)
# except RuntimeError as e:
#     print(f"RuntimeError: {e}")
# print(r2d2._Robot__battery)

# [Абстракція] контракт Participant працює для всіх героїв
# print(olena.greet(r2d2))
# print(r2d2.greet(murka))


# ======================================================================
# 2. НАСЛІДУВАННЯ
# ======================================================================


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

    def move(self):
        return "рухається"

    def introduce(self):
        return f"{self.name} каже: {self.speak()}"


class Mammal(Animal):
    warm_blooded = True

    def move(self):
        return f"ходить → {super().move()}"


class Dog(Mammal):

    @staticmethod
    def speak():
        return "Гав!"


class Cat(Mammal):

    @staticmethod
    def speak():
        return "Няв!"


class FlyingAnimal(Animal):
    def fly(self):
        return f"{self.name} летить"

    def move(self):
        return f"літає → {super().move()}"


# Множинне наслідування: кажан і ссавець, і літає (ромб через Animal)
class Bat(Mammal, FlyingAnimal):
    def speak(self):
        return "Писк!"

    def move(self):
        return f"кажан: {super().move()}"


# rex = Dog("Рекс")
# print(dir(rex))


# tom = Cat("Том")
# print(rex.introduce())
# print(tom.introduce())
# print(rex.warm_blooded, rex.move())
#
# print(isinstance(rex, Animal), isinstance(rex, Mammal), isinstance(rex, FlyingAnimal))
# print(issubclass(Cat, Animal), issubclass(Cat, Dog))
#
# bat = Bat("Бетті")
# print(Bat.__mro__)


# print(bat.introduce())
# print(bat.fly())
# print(bat.move())
# print([c.__name__ for c in Bat.__mro__])
# print(isinstance(bat, Mammal), isinstance(bat, FlyingAnimal))


# ======================================================================
# 3. ПОЛІМОРФІЗМ
# ======================================================================


# participants = [
#     Student("Олена", 19),
#     Dog("Рекс"),
#     Cat("Мурка"),
#     Bat("Бетті"),
# ]
#
# for p in participants:
#     print(p.introduce())

# rex = Dog("Рекс")

# print(isinstance(rex, Cat))
# print(isinstance(rex, Dog))
# print(isinstance(rex, Mammal))
# print(isinstance(rex, Animal))


# ======================================================================
# 4. КОМПОЗИЦІЯ
# ======================================================================


class Battery:
    def __init__(self):
        self._level = 100

    @property
    def level(self):
        return self._level

    def charge(self, percent):
        self._level = min(100, self._level + percent)

    def drain(self, percent):
        if percent > self._level:
            raise RuntimeError("Недостатньо заряду")
        self._level -= percent


# Нова версія Robot: акумулятор тепер окремий об'єкт всередині робота.
# Публічний інтерфейс (battery, charge, work) не змінився


class Participant(ABC):
    @abstractmethod
    def introduce(self):
        pass

    def greet(self, other):
        return f"{self.introduce()}. Радий знайомству, {other.name}!"


class Robot(Participant):
    def __init__(self, name):
        self.name = name
        self._battery = Battery()

    @property
    def battery(self):
        return self._battery.level

    def charge(self, percent):
        self._battery.charge(percent)

    def work(self, hours):
        self._battery.drain(hours * 10)

    def introduce(self):
        return f"Я робот {self.name}, готовий до роботи"


# r2d2 = Robot("r2d2")
# r2d2.work(3)
# print(r2d2.battery)
# r2d2.charge(50)
# print(r2d2.battery)
