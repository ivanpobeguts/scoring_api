import pytest
import redis
import time

from store import RedisStore


@pytest.fixture()
def store():
    store = RedisStore()
    store.cache_set('key', 'value', 60 * 60)
    return store


@pytest.fixture(autouse=True)
def clean_store(store):
    yield
    store.clear()


def test_cache_get_ok(store):
    assert store.cache_get('key') == b'value'


def test_get_ok(store):
    assert store.get('key') == b'value'


def test_get_error():
    store = RedisStore(port=9999, max_retry_count=2, retry_delay=2)
    start_time = time.time()
    with pytest.raises(redis.ConnectionError):
        store.get('key')
    excec_time = time.time() - start_time
    assert excec_time >= 4


def test_cache_get_error():
    store = RedisStore(port=9999, max_retry_count=2, retry_delay=2)
    start_time = time.time()
    with pytest.raises(redis.ConnectionError):
        store.cache_get('key')
    excec_time = time.time() - start_time
    assert excec_time >= 4


def test_cache_set_error():
    store = RedisStore(port=9999, max_retry_count=2, retry_delay=2)
    start_time = time.time()
    with pytest.raises(redis.ConnectionError):
        store.cache_set('key', 'value', 60)
    excec_time = time.time() - start_time
    assert excec_time >= 4
