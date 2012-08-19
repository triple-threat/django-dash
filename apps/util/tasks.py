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
