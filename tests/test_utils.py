import pytest

from utils import check_pairs
from api import OnlineScoreRequest


def test_check_pairs_ok():
    user_info = OnlineScoreRequest(
        phone=71234567890,
        email='adas@sdf'
    )
    assert check_pairs(user_info)