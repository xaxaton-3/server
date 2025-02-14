from django.contrib.auth.models import User
from django.db import models


SUCCESS_STATUS = 'SUCCESS'
INFO_STATUS = 'INFO'
WARNING_STATUS = 'WARNING'
ERROR_STATUS = 'ERROR'


class Notification(models.Model):
    STATUS_CHOICESS = (
        (1, SUCCESS_STATUS),
        (2, INFO_STATUS),
        (3, WARNING_STATUS),
        (4, ERROR_STATUS),
    )

    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICESS)
    received = models.BooleanField(default=False)
