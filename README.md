![django_test](https://github.com/xaxaton-3/server/actions/workflows/tests-runner.yml/badge.svg)

# Red Hot ОГУ Peppers BACKEND
___
## Пошаговая установка и запуск проекта

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
**4. Создать .env файл, содержащий секреты**
Этот файл должен быть в корневой папке. Его содержимое должно выглядеть следующим образом:
```
EMAIL_SENDER=a@gmail.com
EMAIL_PASSWORD=passwordhere
SECRET_KEY=secretkeyhere
DEBUG=True
ALLOWED_HOSTS=*
MISTRAL_TOKEN=tokenhere
```
**5. При запуске на новой базе данных**
```
python manage.py migrate
```
**6. Запустить сервер**
```
python manage.py runserver
```
