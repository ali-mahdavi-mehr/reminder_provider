from django.urls import path
from .views import CreateReminderApiView, DeleteReminderApiView

urlpatterns = [
    path("add-reminder/", CreateReminderApiView.as_view(), name="add-reminder"),
    path("delete-reminder/<int:pk>/" , DeleteReminderApiView.as_view(), name="remove-reminder")
]
