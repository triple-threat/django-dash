import datetime

from util.rediz import connection


class RedisKeyManager(object):

    def _make_generic_key(self, timestamp, prefix):
        return u"{}:{}:{}:{}:{}".format(prefix, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)

    def get_signup_key(self, timestamp):
        return self._make_generic_key(timestamp, 'signup')

    def get_promise_key(self, timestamp):
        return self._make_generic_key(timestamp, 'promise')

    def get_support_key(self, timestamp):
        return self._make_generic_key(timestamp, 'support')

    def get_fb_share_key(self, timestamp):
        return self._make_generic_key(timestamp, 'facebook')

    def get_twitter_share_key(self, timestamp):
        return self._make_generic_key(timestamp, 'twitter')

    def get_poke_key(self, timestamp):
        return self._make_generic_key(timestamp, 'poke')

key_manager = RedisKeyManager()


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

    def log_fb_share(self, data):
        self.redis_log(self.keys.get_fb_share_key)

    def log_twitter_share(self, data):
        self.redis_log(self.keys.get_twitter_share_key)

    def log_poke(self, data):
        self.redis_log(self.keys.get_poke_key)

    def log_promise(self, data):
        self.redis_log(self.keys.get_promise_key)

logger = Logger()
