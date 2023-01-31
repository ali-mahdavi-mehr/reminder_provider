import json
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.views import APIView

from api.models import Reminder
from api.serializer import ReminderSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.generics import DestroyAPIView
import pytz


class CreateReminderApiView(APIView):
    serializer_class = ReminderSerializer

    def post(self, request):
        serialized_data = ReminderSerializer(data=request.data)
        if not serialized_data.is_valid():
            errors = serialized_data.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=errors)
        reminder = serialized_data.save()
        data = serialized_data.data
        reminder_time = datetime.utcnow().replace(minute=data['minute'], hour=data['hour'], second=0, microsecond=0)
        if reminder_time <= datetime.utcnow():
            reminder_time += timedelta(days=1)
        schedule, created = ClockedSchedule.objects.get_or_create(
            clocked_time=reminder_time.replace(tzinfo=pytz.utc)
        )
        try:

            result = PeriodicTask.objects.create(
                clocked=schedule,
                name=f"{data['user']} everyday-at {data['hour']}:{data['minute']} for {'Price' if data['reminder_type'] == 'p' else 'Volume 24'}",
                task='scheduler.tasks.send_message_coin_detail',
                kwargs=json.dumps({
                    "user": data['user'],
                    "coins": data['coins'],
                    "reminder_type": data['reminder_type']
                }),
                one_off=True
            )
        except ValidationError as e:
            return JsonResponse(status=status.HTTP_409_CONFLICT,
                                data={"message": "You already has an alert for this time"})
        except Exception as e:
            print(e)
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": str(e)})
        return JsonResponse({
            "reminder_id": reminder.id,
            "reminder_name": result.name,
        }, status=status.HTTP_201_CREATED)


class DeleteReminderApiView(DestroyAPIView):
    queryset = Reminder.objects.all()
