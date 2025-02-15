from django.contrib.auth.models import User

from users import utils as user_utils


def with_authorization(method):
    def inner(instance, request):
        request = process_request(request)
        return method(instance, request)
    return inner

def process_request(request):
    user = check_authorization(request)
    request.user = user
    return request

def check_authorization(request) -> 'User|None':
        auth_token = request.headers.get('Authorization')
        if auth_token:
            return get_user_by_token(auth_token)
        return None

def get_user_by_token(token: str) -> 'User|None':
    try:
        user, token = user_utils.get_user_by_token(token)
    except Exception:
        return None
    return user
