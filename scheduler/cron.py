import json
from requests import get
from reminder_provider.settings import env
from scheduler.redis_configs import redis_db
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
            for coin in coin_list:
                c = coins_symbols_colors.get(coin["name"], False)
                if coin:
                    coin["symbol"] = c["symbol"]
                    redis_db.set(coin['symbol'], json.dumps(coin))
        else:
            print("lemmon down")
        return True
