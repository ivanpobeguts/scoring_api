import redis

from utils import redis_retry

MAX_RETRY = 5
DELAY = 2


class RedisStore:
    def __init__(self, host='0.0.0.0', port=6379, db=0, socket_connect_timeout=5):
        self.host = host
        self.port = port
        self.db = db
        self.socket_connect_timeout = socket_connect_timeout

    @redis_retry(MAX_RETRY, DELAY)
    def connect(self):
        self.store = redis.Redis(
            host=self.host, port=self.port, db=self.db, socket_connect_timeout=self.socket_connect_timeout
        )

    @redis_retry(MAX_RETRY, DELAY)
    def cache_get(self, key):
        self.store.get(key)

    @redis_retry(MAX_RETRY, DELAY)
    def get(self, key):
        self.store.get(key)

    @redis_retry(MAX_RETRY, DELAY)
    def cache_set(self, key, value, expire):
        self.store.set(key, value, expire)
