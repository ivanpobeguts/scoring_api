def alt_name(name):
    return '_' + name


def prettify_dict(d):
    return ', '.join(f'{k} - {w}' for k, w in d.items())


def check_pairs(user_info):
    if not (user_info.phone and user_info.email) or not (user_info.first_name and user_info.last_name) or not (
            user_info.gender and user_info.birthday):
        return False
    return True