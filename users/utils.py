import datetime
import jwt
import logging
import six

from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import exceptions


AUTHENTICATION_HEADER_PREFIX = 'Bearer'
logger = logging.getLogger(__name__)


def get_user_by_token(auth_header_value: str) -> 'User|None':
    token = auth_header_value.split()
    if len(token) != 2:
        return None

    prefix, value = token
    if prefix != AUTHENTICATION_HEADER_PREFIX:
        return None

    try:
        payload = jwt.decode(
            value, settings.SECRET_KEY, algorithms=['HS256']
        )
    except Exception as e:
        logger.exception(e)
        raise exceptions.AuthenticationFailed('Ошибка аутентификации. Невозможно декодировать токен.')

    try:
        user = User.objects.get(id=payload['id'])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('Пользователь не найден.')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('Пользователь неактивен.')

    return (user, token)


def generate_token(user_id: int):
    token = jwt.encode({'id': user_id}, settings.SECRET_KEY, algorithm="HS256")
    return token
