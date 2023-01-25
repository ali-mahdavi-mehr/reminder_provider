from django.urls import path
from .views import CreateReminderView

urlpatterns = [
    path("add-reminder/", CreateReminderView.as_view(), name="add-reminder"),
]
