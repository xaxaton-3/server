![django_test](https://github.com/xaxaton-3/server/actions/workflows/tests-runner.yml/badge.svg)

# Red Hot ОГУ Peppers BACKEND
___
## Пошаговая установка и запуск проекта

**Наш бекенд может быть развернут с одной из двух СУБД: PostgreSQL или SQLite. Второй вариант, конечно, придуман для подстраховки.**

СУБД по умолчанию: PostgreSQL. Оно и используется при запуске автотестов. Для изменения на SQLite необходимо передать USE_LITE_DB=True в .env

Также, предлагается два способа запуска проекта: через docker-compose и вручную.

___

## Навигация:

<a>Установка:</a> <br>
[1.1 Ручная установка](#11-ручная-установка) <br>
[1.2 Установка через docker-compose](#12-установка-через-docker-compose) <br>
[2 Переменные окружения](#2-наполнение-env-файла) <br>
[3 Создание тестовых пользователей](#3-создание-тестовых-пользователей)

___
## 1.1 Ручная установка
**1. Клонировать репозиторий**
```
git clone https://github.com/xaxaton-3/server.git
```
**2. Создать и активировать виртуальное окружение**
```
python -m venv venv
.\venv\Scripts\activate
```
**3. Установить зависимости**
```
pip install -r requirements.txt
```

**4. Создать .env файл**
```
Пример заполнения см. раздел 2
```

**5. При запуске на новой базе данных**
```
python manage.py migrate
```
**6. Запустить сервер**
```
python manage.py runserver
```

___
## 1.2 Установка через docker-compose
**1. Клонировать репозиторий**
```
git clone https://github.com/xaxaton-3/server.git
```
**2. Создать .env файл**
```
Пример заполнения см. раздел 2
```
**3. Поднять контейнер**
```
docker-compose up --build -d && docker-compose logs -f
```
**3.1. При необходимости отключения:**
```
docker-compose down --remove-orphans
```


___

## 2 Наполнение .env файла
```
# .env файл имеет приоритет над установленными в среде переменными окружения.
USE_LITE_DB=False  # True - запуск с SQLite, False - запуск с PostgreSQL
EMAIL_SENDER=a@gmail.com  # почта, с которой происходит рассылка писем. Передадим данные через модератора.
EMAIL_PASSWORD=passwordhere  # пароль от почты, с которой происходит рассылка писем. Передадим данные через модератора.
SECRET_KEY=secretkeyhere
DEBUG=True
ALLOWED_HOSTS=*
MISTRAL_TOKEN=tokenhere
# Укажите свои данные ниже:
POSTGRES_HOST=db
POSTGRES_DB=fatherland_defender
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
# При USE_LITE_DB = True можно не указывать.
```

___

## 3 Создание тестовых пользователей
Создаются пользователи: admin@mail.ru 12345 и user@mail.ru 12345.
```
python manage.py init_user
```