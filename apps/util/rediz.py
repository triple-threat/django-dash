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

import redis
from django.conf import settings


connection = redis.from_url(settings.REDIS_CONNECTION)


def get_support_key(profile_id):
    return unicode("{}:supports").format(profile_id)


def get_promise_key(profile_id):
    return unicode("{}:promises").format(profile_id)


def get_ids_from_redis(key):
    ids = connection.lrange(key, 0, -1)
    if ids:
        return [int(x) for x in ids]
    else:
        return []
