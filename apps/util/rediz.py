import redis

from django.conf import settings


class ConnectionManager(object):
    connection_dict = {}

    def get_connection(self, name=None):
        name = name or "default"

        try:
            config = settings.REDIS_CONNECTIONS[name]
        except KeyError:
            raise ValueError("No redis connections named %s in settings" % name)

        if self.connection_dict.get(name):
            return self.connection_dict.get(name)

        host = config['HOST']
        port = config['PORT']
        conn = redis.StrictRedis(host=host, port=port)
        self.connection_dict[name] = conn

        return conn

    @property
    def stable(self):
        return self.get_connection('stable')

    @property
    def unstable(self):
        return self.get_connection('unstable')

    @property
    def logging(self):
        return self.get_connection('logging')

connection = ConnectionManager()


def get_support_key(profile_id):
    return unicode("{}:supports").format(profile_id)
