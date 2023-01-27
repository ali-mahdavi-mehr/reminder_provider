import asyncio
import json
from datetime import datetime
from celery import shared_task
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from telegram import Bot
from reminder_provider.settings import env
from scheduler.redis_configs import redis_db
from utils.price_generator import price_seperator




async def send_coin_detail_message(user, coins):
    text = "your alert is triggered\n"
    bot = Bot(env("TELEGRAM_TOKEN"))
    coins = [coin.strip(" ") for coin in coins.split(",")]
    for coin in coins:
        c = redis_db.get(coin) or json.dumps({"name": "ali", "price": "1322323"})
        c = json.loads(c)
        text += f"{coin} ({c['name']}) => {price_seperator(c['price'])}$\n"

    await bot.send_message(chat_id=user, text=text)


@shared_task
def send_message_coin_detail(user: str, coins: str):
    asyncio.run(send_coin_detail_message(user, coins))
    return True


@shared_task
def update_schedules_for_tomorrow():
    now = datetime.utcnow()
    ClockedSchedule.objects.filter(clocked_time__lt=datetime.utcnow()).update(
        clocked_time__year=now.year,
        clocked_time__month=now.month,
        clocked_time__day=now.day
    )
    PeriodicTask.objects.filter(enabled=False).update(enabled=True)



