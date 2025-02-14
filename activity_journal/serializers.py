from rest_framework import serializers

from activity_journal.models import Journal


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'
