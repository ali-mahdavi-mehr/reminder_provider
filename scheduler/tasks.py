import asyncio
import json
from celery import shared_task
from telegram import Bot

from public.constant import REDIS_COIN_DB
from reminder_provider.settings import env
from scheduler.redis_configs import RedisConnection
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

