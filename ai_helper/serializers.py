from rest_framework import serializers

from django.conf import settings


class AiTextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=settings.MAX_PERSON_HISTORY_LENGTH)
