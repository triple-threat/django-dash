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

from emailer.tasks import send_support_email
from event.keys import key_manager


class Logger(object):

    conn = connection
    keys = key_manager

    def increment(self, key):
        self.conn.incr(key, 1)

    def redis_log(self, get_key):
        timestamp = datetime.datetime.now()
        self.increment(get_key(timestamp))

    def log(self, logger, data={}):
        handler = getattr(self, "log_{}".format(logger))
        handler(data)

    def log_signup(self, data):
        self.redis_log(self.keys.get_signup_key)

    def log_support(self, data):
        self.redis_log(self.keys.get_support_key)
        supporter_id = data.get('supporter_id')
        promise_id = data.get('promise_id')
        send_support_email(supporter_id, promise_id)

    def log_facebook_share(self, data):
        self.redis_log(self.keys.get_facebook_share_key)

    def log_twitter_share(self, data):
        self.redis_log(self.keys.get_twitter_share_key)

    def log_poke(self, data):
        self.redis_log(self.keys.get_poke_key)

    def log_promise(self, data):
        self.redis_log(self.keys.get_promise_key)

logger = Logger()
