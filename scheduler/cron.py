import json
from datetime import datetime
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from requests import get

from public.constant import REDIS_COIN_DB
from reminder_provider.settings import env
from scheduler.redis_configs import get_redis_db
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
            redis_db = get_redis_db(REDIS_COIN_DB)
            result = json.loads(response.text)
            coin_list = result["coinsList"]
            for coin in coin_list:
                c = coins_symbols_colors.get(coin["name"], False)
                if c:
                    coin["symbol"] = c["symbol"]
                    redis_db.set(coin['symbol'], json.dumps(coin))
        else:
            print("lemmon down")


class UpdateReminders(CronJobBase):
    RUN_AT_TIMES = ['23:59', "11:59"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cronjob.UpdateReminders'

    def do(self):
        print("update coins")
        now = datetime.utcnow()
        ClockedSchedule.objects.filter(clocked_time__lt=datetime.utcnow()).update(
            clocked_time__year=now.year,
            clocked_time__month=now.month,
            clocked_time__day=now.day
        )
        PeriodicTask.objects.filter(enabled=False).update(enabled=True)
