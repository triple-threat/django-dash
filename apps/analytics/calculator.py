import datetime

from util.rediz import connection
from event.keys import key_manager


class MetricDataFetcher(object):
    def __init__(self, metric_name, hours_before):
        self.metric_name = metric_name
        self.hours_before = int(hours_before)

    def get_timestamps(self):
        now = datetime.datetime.now()
        before = now - datetime.timedelta(hours=self.hours_before)
        minutes = self.hours_before * 60
        return [before + datetime.timedelta(minutes=x) for x in range(minutes)]

    def get_timestamps_and_redis_keys(self):
        timestamps = self.get_timestamps()
        return [(ts, key_manager.get_key(self.metric_name, ts)) for ts in timestamps]

    def get_redis_data(self):
        ts_and_keys = self.get_timestamps_and_redis_keys()
        return {ts: self.transform(connection.get(key)) for ts, key in ts_and_keys}

    def transform(self, val):
        return int(val) if val else 0

