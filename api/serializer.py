from rest_framework.serializers import ModelSerializer
from api.models import Reminder


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
