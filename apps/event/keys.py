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


class RedisKeyManager(object):
    """
    A simple layer of abstraction around storing the metric data in Redis.
    """

    def _make_generic_key(self, timestamp, prefix):
        return u"{}:{}:{}:{}:{}".format(prefix, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)

    def get_key(self, metric_name, timestamp):
        handler = getattr(self, 'get_{}_key'.format(metric_name))
        return handler(timestamp)

    def get_signup_key(self, timestamp):
        return self._make_generic_key(timestamp, 'signup')

    def get_promise_key(self, timestamp):
        return self._make_generic_key(timestamp, 'promise')

    def get_support_key(self, timestamp):
        return self._make_generic_key(timestamp, 'support')

    def get_facebook_share_key(self, timestamp):
        return self._make_generic_key(timestamp, 'facebook_share')

    def get_twitter_share_key(self, timestamp):
        return self._make_generic_key(timestamp, 'twitter_share')

    def get_poke_key(self, timestamp):
        return self._make_generic_key(timestamp, 'poke')

key_manager = RedisKeyManager()
