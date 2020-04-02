import time
import logging
import redis


def alt_name(name):
    return '_' + name


def prettify_dict(d):
    return ', '.join(f'{k} - {w}' for k, w in d.items())


def check_pairs(user_info):
    if not any([(user_info.phone and user_info.email), (user_info.first_name and user_info.last_name),
               (user_info.gender is not None and user_info.birthday)]):
        return False
    return True


def redis_retry(func):
    def wrapper(self, *args, **kwargs):
        count = 0
        while True:
            try:
                return func(self, *args, **kwargs)
            except redis.ConnectionError:
                logging.warning('Cannot connect to localhost:6379. Trying again in 2 seconds...')
                count += 1
                if count > self.max_retry_count:
                    raise
                time.sleep(self.retry_delay)

    return wrapper
