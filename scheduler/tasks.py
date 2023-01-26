import asyncio
import json
from datetime import timedelta, datetime

from celery import shared_task
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from telegram import Bot
from scheduler.redis_configs import redis_db
import os
import environ
from django.db.models import F
from reminder_provider.settings import BASE_DIR

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


async def send(user, coins):
    text = "your alert is triggered\n"
    bot = Bot(env("TELEGRAM_TOKEN"))
    coins = [coin.strip(" ") for coin in coins.split(",")]
    for coin in coins:
        c = redis_db.get(coin) or json.dumps({"name": "ali", "price": "1322323"})
        c = json.loads(c)
        text += f"{coin} ({c['name']}) => {c['price']}\n"

    await bot.send_message(chat_id=user, text=text)


@shared_task
def send_message(user: str, coins: str):
    asyncio.run(send(user, coins))
    return True


@shared_task
def update_for_tommorow():
    ClockedSchedule.objects.filter(clocked_time__lt=datetime.utcnow()).update(clocked_time=F('clocked_time') + timedelta(days=1))
    PeriodicTask.objects.filter(enabled=False).update(enabled=True)



