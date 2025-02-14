from django.contrib.auth.models import User
from django.db import models


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
