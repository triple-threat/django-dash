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
