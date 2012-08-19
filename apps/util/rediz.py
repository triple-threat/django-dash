import redis
from django.conf import settings


connection = redis.from_url(settings.REDIS_CONNECTION)


def get_support_key(profile_id):
    return unicode("{}:supports").format(profile_id)


def get_promise_key(profile_id):
    return unicode("{}:promises").format(profile_id)


def get_ids_from_redis(key):
    return [int(x) for x in connection.lrange(key, 0, -1)]
