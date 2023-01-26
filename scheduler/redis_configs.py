import os

import environ
from redis import Redis

from reminder_provider.settings import BASE_DIR

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

redis_db = Redis.from_url(env("REDIS_URL"))

