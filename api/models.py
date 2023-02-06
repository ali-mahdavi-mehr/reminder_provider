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
    PRODUCER_TYPES = (
        ("l", "Luna"),
        ("v", "Venus")
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
    producer = models.CharField(max_length=100, choices=PRODUCER_TYPES, default="l")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} {self.reminder_type} {self.hour}:{self.minute} {self.producer}"
