class RedisKeyManager(object):

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
