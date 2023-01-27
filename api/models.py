from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from api.manager import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()


    username = None
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS[:]
    REQUIRED_FIELDS.remove('email')
    USERNAME_FIELD = 'email'


class Reminder(models.Model):
    REMINDER_TYPES = (
        ("p", "PRICE"),
        ("v", "VOLUME")
    )
    reminder_type = models.CharField(max_length=1, choices=REMINDER_TYPES, default="p")
    user = models.CharField(max_length=100)
    coins = models.TextField()
    hour = models.IntegerField(
        validators=[
            MaxValueValidator(23),
            MinValueValidator(0)
        ]
    )
    minute = models.IntegerField(
        validators=[
            MaxValueValidator(59),
            MinValueValidator(0)
        ]
    )
