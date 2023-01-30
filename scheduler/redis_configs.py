from redis import Redis

from reminder_provider.settings import env


def get_redis_db(db=0):
    redis_db = Redis.from_url(env("REDIS_URL"), db=db)
    return redis_db

