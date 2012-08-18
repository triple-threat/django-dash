import redis
from django.conf import settings


connection = redis.from_url(settings.REDIS_CONNECTION)


def get_support_key(profile_id):
    return unicode("{}:supports").format(profile_id)
