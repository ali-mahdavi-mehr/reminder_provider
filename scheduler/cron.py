import json
import time
from datetime import datetime

import pytz
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from requests import get

from api.models import Reminder
from public.constant import REDIS_COIN_DB
from reminder_provider.settings import env
from scheduler.redis_configs import RedisConnection
from django_cron import CronJobBase, Schedule
from scheduler.symbols import coins_symbols_colors


class UpdateCoins(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cronjob.update_coins'

    def do(self):
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


class UpdateReminders(CronJobBase):
    RUN_AT_TIMES = ['23:59',]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cronjob.UpdateReminders'

    def do(self):
        now = datetime.utcnow()
        # TODO: Better solution must be considered
        for item in Reminder.objects.filter(is_active=True, producer="l"):
            reminder_time = datetime.utcnow().replace(minute=item.minute, hour=item.hour, second=0, microsecond=0, day=now.day +1)
            schedule, created = ClockedSchedule.objects.get_or_create(
                clocked_time=reminder_time.replace(tzinfo=pytz.utc)
            )
            PeriodicTask.objects.create(
                clocked=schedule,
                name=f"{item.user} everyday-at {item.hour}:{item.minute} for {'Price' if item.reminder_type == 'p' else 'Volume 24'} created at {time.time()}",
                task='scheduler.tasks.send_message_coin_detail',
                kwargs=json.dumps({
                    "user": item.user,
                    "coins": item.coins,
                    "reminder_type": item.reminder_type
                }),
                one_off=True
            )
