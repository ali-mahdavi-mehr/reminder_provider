from redis import Redis

from reminder_provider.settings import env


class RedisConnection:
    def __init__(self, connection_url=env("REDIS_URL"), db: int = 0):
        self.connection_url = connection_url
        self.db = db

    def __enter__(self):
        self.conn = Redis.from_url(self.connection_url, db=self.db, decode_responses=True)
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()
