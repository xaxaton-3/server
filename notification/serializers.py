from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=120, required=False)

    class Meta:
        model = Notification
        fields = ['id', 'email', 'to_user', 'message', 'status']

    def create(self, validated_data):
        if validated_data.get('email'):
            validated_data.pop('email')
        return super().create(validated_data)
