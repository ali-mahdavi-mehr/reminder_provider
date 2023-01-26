from redis import Redis

from reminder_provider.settings import env


redis_db = Redis.from_url(env("REDIS_URL"))

