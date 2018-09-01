# Задание 1. Встроенные типы данных, операторы, функции и генераторы
#
# Напишите реализации объявленных ниже функций. Для проверки
# корректности реализации ваших функций, запустите тесты:
#
# pytest test_homework01.py
#
# Если написанный вами код не содержит синтаксических ошибок,
# вы увидите результаты тестов ваших решений.


class call_count:
    def __init__(self, func):
        self.__count = 0
        self.__func = func

    def __call__(self, *args, **kwargs):
        self.__count += 1
        result = self.__func(*args, **kwargs)
        return result

    @property
    def call_count(self):
        return self.__count


def fac(n):
    """
    Факториал

    Факториал числа N - произведение всех целых чисел от 1 до N
    включительно. Например, факториал числа 5 - произведение
    чисел 1, 2, 3, 4, 5.

    Функция должна вернуть факториал аргумента, числа n.
    """
    if n <= 0:
        return 1
    else:
        return n * fac(n - 1)


def gcd(a, b):
    """
    Наибольший общий делитель (НОД) для двух целых чисел.

    Предполагаем, что оба аргумента - положительные числа
    Один из самых простых способов вычесления НОД - метод Эвклида,
    согласно которому

    1. НОД(a, 0) = a
    2. НОД(a, b) = НОД(b, a mod b)

    (mod - операция взятия остатка от деления, в python - оператор '%')
    """
    while b != 0:
        a, b = b, a % b
    return a


def fib():
    """
    Генератор для ряда Фибоначчи

    Вам необходимо сгенерировать бесконечный ряд чисел Фибоначчи,
    в котором каждый последующий элемент ряда является суммой двух
    предыдущих. Начало последовательности: 1, 1, 2, 3, 5, 8, 13, ..

    Подсказка по реализации: для бесконечного цикла используйте идиому

    while True:
      ..

    """
    a, b = 1, 1
    yield a
    while True:
        yield b
        a, b = b, a + b


def flatten(seq):
    """
    Функция, преобразующая вложенные последовательности любого уровня
    вложенности в плоские, одноуровневые.

    >>> flatten([])
    []
    >>> flatten([1, 2])
    [1, 2]
    >>> flatten([1, [2, [3]]])
    [1, 2, 3]
    >>> flatten([(1, 2), (3, 4)])
    [1, 2, 3, 4]
    """
    for item in seq:
        try:
            yield from flatten(item)
        except TypeError:
            yield item