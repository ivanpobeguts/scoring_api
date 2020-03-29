import json
import pytest
from mock import Mock
import redis

from scoring import get_score, get_interests


def test_get_score_with_cache_data():
    store = Mock()
    store.cache_get.return_value = 10
    score = get_score(store, None, None)
    assert score == 10


def test_get_score_without_cache_data():
    store = Mock()
    store.cache_get.return_value = None
    score = get_score(store, 71234567890, 'email@com', '01.10.2016')
    assert score == 3


def test_get_score_cache_connection_error():
    store = Mock()
    store.cache_get.side_effect = redis.ConnectionError()
    score = get_score(store, 71234567890, 'email@com', '01.10.2016')
    assert score == 3


def test_get_interests_with_store():
    cid = 1
    interests = '{"dogs": 1}'
    store = {f'i:{cid}': interests}
    assert get_interests(store, 1) == json.loads(interests)


def test_get_interests_without_store():
    store = Mock()
    store.get.side_effect = redis.ConnectionError()
    with pytest.raises(Exception):
        get_interests(store, 1)
