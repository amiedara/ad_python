"""
URL shortener.

Supported schemes: http, https.
"""

from django.conf import settings
from django.core.cache import cache
from django.conf.urls import url
from django.http import HttpResponse
from urllib.parse import urlparse
from django.shortcuts import redirect
import random, string

# Задание 2. URL shortener
#
# Реализуйте сервис для сокращения ссылок. Примеры таких сервисов:
# http://bit.ly, http://t.co, http://goo.gl
# Пример ссылки: http://bit.ly/1qJYR0y
#
# Вам понадобится реализовать функции
#  - для генерации ключа
#  - для обработки запроса для сабмита URL
#  - для редиректа с короткого URL на исходный.
#
# Для хранения соответствий наших коротких ключей и полных URL
# мы будем использовать кеш Django, django.core.cache
# Экземпляр cache уже импортирован, и используется следующим образом.
# Сохранить значение:
#
#  cache.add(key, value)
#
# Извлечь значение:
#
#  cache.get(key, default_value)
#
# Второй, опциональный аргумент метода get - значение по умолчанию,
# если ключ не найден в кеше.
#
# Для проверки корректности реализации ваших функций,
# запустите тесты на выполнение:
#
# pytest test_homework02.py
#
# Также вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework02.py runserver

counter_dict = {}

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
    )


def random_key():
    """
    Случайный короткий ключ, состоящий из цифр и букв.
    Минимальная длина ключа - 5 символов. Для генерации случайных
    последовательностей вы можете воспользоваться библиотекой random.
    """
    return ''.join(random.choice(''.join((string.ascii_letters, string.digits))) for _ in range(random.randint(5, 20)))


def index(request):
    """
    Index. Главная страница
    """
    return HttpResponse(__doc__)


def shorten(request, url):
    """
    1. Проверяем URL. Допускаются следующие схемы: http, https
    Подсказка: разобрать URL можно функцией urllib.parse.urlparse
    Если URL не прошел проверку - редирект на главную.

    Если URL прошел проверку:

    2. Сохраняем URL в кеш со сгенерированным ключом:

    cache.add(key, url)

    4. Отдаем успешный ответ с кодом в теле ответа.
    Удобно, если это будет кликабельная ссылка (HTML тег 'a') вида
    <a href="http://localhost:8000/ключ">ключ</a>
    """
    o = urlparse(url)
    if o.scheme in ('http', 'https'):
        key = random_key()
        cache.add(key, url)
        return HttpResponse('<a href="http://localhost:8000/{0}">{0}</a>'.format(key))
    else:
        return redirect('/')


def redirect_view(request, key):
    """
    Редирект

    Функция обрабатывает сокращенный URL вида http://localhost:8000/ключ
    Ищем ключ в кеше (cache.get). Если ключ не найден, редиректим на главную страницу (/)
    Если найден, редиректим на полный URL, сохраненный под данным ключом.
    Для редиректа можете воспользоваться вспомогательной функцией
    django.shortcuts.redirect(redirect_to) или классом-наследником HttpResponse
    """
    if key in cache:
        return redirect(cache.get(key))
    else:
        if key in counter_dict:
            counter_dict[key] += 1
        else:
            counter_dict[key] = 1
        return redirect('/')


def urlstats(request, key):
    """
    (Опционально)

    Реализуйте счетчик кликов на сокращенные ссылки.
    В теле ответа функция должна возращать количество
    переходов по данному коду.
    """
    if key in counter_dict:
        return HttpResponse(counter_dict[key])
    else:
        return HttpResponse('1')


urlpatterns = [
    url(r'^$', index),
    # http://localhost:8000/shorten/<url>
    url(r'shorten/(.+)$', shorten),
    # http://localhost:8000/urlstats/<key>
    url(r'urlstats/([\w\d]+)$', urlstats),
    # http://localhost:8000/<key>
    url(r'([\w\d]+)', redirect_view),
]

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

print(urlstats(4, 424324))
