from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.views import APIView
from api.serializer import ReminderSerializer
from django.http.response import JsonResponse


class CreateReminderView(APIView):
    serializer_class = ReminderSerializer

    def post(self, request):
        data = request.POST
        reminder_time = datetime.utcnow().replace(minute=int(data["minute"]), hour=int(data["hour"]), second=0,
                                                  microsecond=0)
        if reminder_time <= datetime.utcnow():
            reminder_time = reminder_time.replace(
                day=datetime.utcnow() + timedelta(days=1)
            )

        schedule, created = ClockedSchedule.objects.get_or_create(
            clocked_time=reminder_time
        )
        result = PeriodicTask.objects.create(
            clocked=schedule,
            name=f"{data['user']}-everyday-at {data['hour']}:{data['minute']}",
            task='scheduler.tasks.send_message_coin_detail',
            args=(data['user'], data['coins']),
            one_off=True
        )

        return JsonResponse({
            "id": result.id,
            "name": result.name
        }, status=200)
