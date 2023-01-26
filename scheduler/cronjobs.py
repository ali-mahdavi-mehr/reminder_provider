import json
import os
from requests import get
import environ

from reminder_provider.settings import BASE_DIR
from scheduler.redis_configs import redis_db

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os().path.join(BASE_DIR, '.env'))


def update_coins():
    print("hi lemmon")
    url = env("LEMMON_API")
    response = get(url)
    if response.status_code == 200:
        result = json.loads(response.text)
        coin_list = result["coinsList"]
        for coin in coin_list:
            redis_db.set(coin['symbol'], json.dumps(coin))
    else:
        print("lemmon down")
    print("coins updated")
    return True