from api.models import Reminder
from rest_framework import serializers


class ReminderSerializer(serializers.ModelSerializer):
    hour = serializers.IntegerField(required=True, max_value=23, min_value=0)
    minute = serializers.IntegerField(required=True, max_value=59, min_value=0)
    class Meta:
        model = Reminder
        fields = '__all__'
