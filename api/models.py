from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Reminder(models.Model):
    user = models.CharField(max_length=100)
    coins = models.TextField()
    hour = models.IntegerField()
    minute = models.IntegerField()
