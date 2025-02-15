from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создаются тестовые пользователи: admin@mail.ru 12345 и user@mail.ru 12345'

    def create_user(self, email: str, password: str):
        try:
            user = User.objects.get(email=email)
            return None
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=email)
            user.set_password(password)
            user.save(update_fields=['password'])
            return user
        
    def handle(self, *args, **kwargs):
        admin = self.create_user('admin@mail.ru', '12345')
        user = self.create_user('user@mail.ru', '12345')
        if not admin:
            self.stdout.write(self.style.WARNING('Admin with this email already exists'))
        else:
            admin.is_superuser = True
            admin.save(update_fields=['is_superuser'])
        if not user:
            self.stdout.write(self.style.WARNING('User with this email already exists'))

        self.stdout.write(self.style.SUCCESS('Finish init_user command'))
