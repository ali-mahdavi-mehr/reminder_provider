from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.views import APIView
from api.serializer import ReminderSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.generics import DestroyAPIView


class CreateReminderApiView(APIView):
    serializer_class = ReminderSerializer

    def post(self, request):
        serialized_data = ReminderSerializer(data=request.data)
        if not serialized_data.is_valid():
            errors = serialized_data.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=errors)
        data = serialized_data.data
        reminder_time = datetime.utcnow().replace(minute=data['minute'], hour=data['hour'], second=0, microsecond=0)
        if reminder_time <= datetime.utcnow():
            reminder_time = reminder_time.replace(
                day=datetime.utcnow() + timedelta(days=1)
            )
        schedule, created = ClockedSchedule.objects.get_or_create(
            clocked_time=reminder_time
        )
        try:

            result = PeriodicTask.objects.create(
                clocked=schedule,
                name=f"{data['user']}-everyday-at {data['hour']}:{data['minute']}",
                task='scheduler.tasks.send_message_coin_detail',
                args=(data['user'], data['coins']),
                one_off=True
            )
        except ValidationError as e:
            return JsonResponse(status=status.HTTP_409_CONFLICT,
                                data={"message": "You already has an alert for this time"})

        return JsonResponse({
            "reminder_id": result.id,
            "reminder_name": result.name
        }, status=status.HTTP_201_CREATED)


class DeleteReminderApiView(DestroyAPIView):
    queryset =  PeriodicTask.objects.all()