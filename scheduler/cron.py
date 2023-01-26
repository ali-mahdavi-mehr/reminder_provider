import json
# import os
from requests import get
# import environ
# from reminder_provider.settings import BASE_DIR
from scheduler.redis_configs import redis_db
from django_cron import CronJobBase, Schedule

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
#
# environ.Env.read_env(os().path.join(BASE_DIR, '.env'))
from scheduler.symbols import coins_symbols_colors


class UpdateCoins(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cronjob.update_coins'

    def do(self):
        print("updating coins")
        url = "https://portfoliotracker.b4a.app/get-all-coins"
        response = get(url)
        if response.status_code == 200:
            result = json.loads(response.text)
            coin_list = result["coinsList"]
            print("coins received")
            for coin in coin_list:
                c = coins_symbols_colors.get(coin["name"], False)
                if coin:
                    coin["symbol"] = c["symbol"]
                    redis_db.set(coin['symbol'], json.dumps(coin))
        else:
            print("lemmon down")
        print("coins updated")
        return True
