import redis

from utils import redis_retry

MAX_RETRY = 5


class RedisStore:
    def __init__(self):
        self.connect()

    @redis_retry(MAX_RETRY)
    def connect(self):
        self.store = redis.Redis(host='0.0.0.0', port=6379, db=0, socket_connect_timeout=5)

    @redis_retry(MAX_RETRY)
    def cache_get(self, key):
        self.store.get(key)

    @redis_retry(MAX_RETRY)
    def get(self, key):
        self.store.get(key)

    @redis_retry(MAX_RETRY)
    def cache_set(self, key, value, expire):
        self.store.set(key, value, expire)