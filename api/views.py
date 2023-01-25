from celery.result import AsyncResult
# from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.views import APIView

from api.serializer import ReminderSerializer
from scheduler import celery
from django.http import HttpResponse
from scheduler.celery import debug_task


class CreateReminderView(APIView):
    serializer_class = ReminderSerializer

    def post(self, request):
        result = celery.debug_task.delay(9, 9)
        return HttpResponse(f"{result}", status=200)
