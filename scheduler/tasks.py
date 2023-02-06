import asyncio
import json
from datetime import datetime
import time

import pytz
from celery import shared_task
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from requests import get
from telegram import Bot

from api.models import Reminder
from public.constant import REDIS_COIN_DB
from reminder_provider.settings import env
from scheduler.redis_configs import RedisConnection
from scheduler.symbols import coins_symbols_colors
from utils.price_generator import price_seperator, number_generator


async def send_coin_detail_message(user, coins, reminder_type):
    text = f"{'Price' if reminder_type == 'p' else 'Volume'} Reminder 🔔\n"
    bot = Bot(env("TELEGRAM_TOKEN"))
    coins = [coin.strip(" ") for coin in coins.split(",")]
    with RedisConnection(db=REDIS_COIN_DB) as redis_db:
        for coin in coins:
            c = redis_db.get(coin) or json.dumps({"name": "ali", "price": "0"})
            c = json.loads(c)
            amount = 0
            if reminder_type == "p":
                amount = f"{price_seperator(c.get('price', 0))}$"
            elif reminder_type == "v":
                amount = f"${number_generator(c.get('volume_24h', 0))}"
            text += f"{coin} ({c['name']}): {amount}\n"

    await bot.send_message(chat_id=user, text=text)


@shared_task
def send_message_coin_detail(user: str, coins: str, reminder_type: str):
    asyncio.run(send_coin_detail_message(user, coins, reminder_type))
    return True


@shared_task
def add_reminders_for_tomorrow():
    now = datetime.utcnow()
    periodic_tasks = list()
    for item in Reminder.objects.filter(is_active=True, producer="l"):
        print("item", item)
        reminder_time = datetime.utcnow().replace(minute=item.minute, hour=item.hour, second=0, microsecond=0,
                                                  day=now.day + 5)
        schedule = ClockedSchedule.objects.create(
            clocked_time=reminder_time.replace(tzinfo=pytz.utc)
        )
        periodic_task = PeriodicTask(
            clocked=schedule,
            name=f"{item.user}-{item.hour}:{item.minute}-{'Price' if item.reminder_type == 'p' else 'Volume 24'}-{time.time()}",
            task='scheduler.tasks.send_message_coin_detail',
            kwargs=json.dumps({
                "user": item.user,
                "coins": item.coins,
                "reminder_type": item.reminder_type
            }),
            one_off=True
        )
        periodic_tasks.append(periodic_task)

    PeriodicTask.objects.bulk_create(periodic_tasks)



@shared_task
def update_coins():
    url = env("LEMMON_API")
    response = get(url)
    if response.status_code == 200:
        result = json.loads(response.text)
        coin_list = result["coinsList"]
        with RedisConnection(db=REDIS_COIN_DB) as redis_db:
            for coin in coin_list:
                c = coins_symbols_colors.get(coin["name"], False)
                if c:
                    coin["symbol"] = c["symbol"]
                    redis_db.set(coin['symbol'], json.dumps(coin))
    else:
        print("lemmon down")



