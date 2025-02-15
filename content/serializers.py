from rest_framework import serializers

from content.models import Defender


class DefenderFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defender
        fields = ['id', 'meta']


class DefenderFormDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defender
        fields = ['id']
