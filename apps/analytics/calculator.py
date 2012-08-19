# Promise.ly -- social commitment platform
#
# Copyright (C) 2012  Promise.ly authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

