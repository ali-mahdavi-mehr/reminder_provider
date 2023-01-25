from __future__ import absolute_import

import os
import sys

from celery import Celery

from django.conf import settings
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder_provider.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')
django.setup()

app = Celery("scheduler")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(*args, **kwargs):
    print("hi\n")
    # print(f'Request: {self.request!r}')
