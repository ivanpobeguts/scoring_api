import pytest

from utils import check_pairs
from api import OnlineScoreRequest


@pytest.mark.parametrize(
    'phone, email, first_name, last_name, gender, birthday',
    [
        (71234567890, 'adas@sdf', None, None, None, None),
        (71234567890, 'adas@sdf', 'Ivan', 'Ivanov', None, None),
        (None, None, 'Ivan', 'Ivanov', None, None),
        (None, None, 'Ivan', 'Ivanov', 2, '20.09.2017'),
        (None, None, None, None, 1, '20.09.2017'),
        (None, None, None, None, 0, '20.09.2017'),
        (71234567890, 'adas@sdf', None, None, 0, '20.09.2017'),
        (71234567890, 'adas@sdf', 'Ivan', 'Ivanov', 2, '20.09.2017'),
    ]
)
def test_check_pairs_ok(phone, email, first_name, last_name, gender, birthday):
    user_info = OnlineScoreRequest(
        phone=phone,
        email=email,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthday=birthday
    )
    assert check_pairs(user_info)


@pytest.mark.parametrize(
    'phone, email, first_name, last_name, gender, birthday',
    [
        (71234567890, '', None, None, None, None),
        (71234567890, None, 'Ivan', '', None, None),
        (None, None, '', 'Ivanov', None, None),
        (None, None, None, None, 0, ''),
        ('', 'adas@sdf', None, None, None, '20.09.2017'),
        ('', 'adas@sdf', None, '123', 1, ''),
    ]
)
def test_check_pairs_not_ok(phone, email, first_name, last_name, gender, birthday):
    user_info = OnlineScoreRequest(
        phone=phone,
        email=email,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthday=birthday
    )
    assert not check_pairs(user_info)