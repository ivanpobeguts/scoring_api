import redis

from utils import redis_retry


class RedisStore:

    MAX_RETRY = 5
    DELAY = 2

    def __init__(self, host='0.0.0.0', port=6379, db=0, socket_connect_timeout=5, max_retry_count=MAX_RETRY, retry_delay=DELAY):
        self.max_retry_count = max_retry_count
        self.retry_delay = retry_delay
        self.store = redis.Redis(
            host=host, port=port, db=db, socket_connect_timeout=socket_connect_timeout
        )

    @redis_retry
    def cache_get(self, key):
        return self.store.get(key)

    @redis_retry
    def get(self, key):
        return self.store.get(key)

    @redis_retry
    def cache_set(self, key, value, expire):
        self.store.set(key, value, expire)

    @redis_retry
    def clear(self):
        self.store.flushdb()
