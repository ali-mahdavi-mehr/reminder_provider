from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.views import APIView
from api.serializer import ReminderSerializer
from django.http.response import JsonResponse


class CreateReminderView(APIView):
    serializer_class = ReminderSerializer
    def post(self, request):
        data = request.POST
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )
        result = PeriodicTask.objects.create(
            interval=schedule,  # we created this above.
            name=f"{data['user']}-everyday-at {data['hour']}:{data['minute']}",  # simply describes this periodic task.
            task='scheduler.tasks.send_message',
            args=data['coins']
        )
        return JsonResponse({
            "id": result.id,
            "name": result.name
        }, status=200)
