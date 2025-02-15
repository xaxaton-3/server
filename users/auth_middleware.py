from django.contrib.auth.models import User

from users import utils as user_utils


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = self.check_authorization(request)
        response.user = user
        return response

    def check_authorization(self, request) -> 'User|None':
        auth_token = request.headers.get('Authorization')
        if auth_token:
            return self.get_user_by_token(auth_token)
        return None

    def get_user_by_token(self, token: str) -> 'User|None':
        return user_utils.get_user_by_token(token)
