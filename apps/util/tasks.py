from util.rediz import get_support_key, get_promise_key, connection

from promise.models import Promise


def refill_redis(profile_id):
    support_key = get_support_key(profile_id)
    promise_key = get_promise_key(profile_id)
    promise_ids = list(Promise.objects.filter(creator=profile_id).active().values_list('id', flat=True))
    connection.delete(promise_key)
    for prom_id in promise_ids:
        connection.lpush(promise_key, prom_id)
    promises_supported_ids = list(Promise.objects.filter(supporter__id=profile_id).values_list('id', flat=True))
    connection.delete(support_key)
    for prom_id in promises_supported_ids:
        connection.lpush(support_key, prom_id)
