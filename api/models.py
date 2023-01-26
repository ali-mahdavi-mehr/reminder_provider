from django.db import models
from django.contrib.auth.models import AbstractUser

from api.manager import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()


    username = None
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS[:]
    REQUIRED_FIELDS.remove('email')
    USERNAME_FIELD = 'email'


class Reminder(models.Model):
    user = models.CharField(max_length=100)
    coins = models.TextField()
    hour = models.IntegerField()
    minute = models.IntegerField()
