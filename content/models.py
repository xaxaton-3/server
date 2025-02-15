from django.db import models


class Defender(models.Model):
    meta = models.JSONField(default=dict)
    is_open = models.BooleanField(default=True)
