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

from django.db import models


class PromiseManager(models.Manager):

    def get_query_set(self):
        return PromiseQuerySet(self.model)


class PromiseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1)

    def expired(self):
        return self.filter(status__in=[2, 3])

    def successful(self):
        return self.filter(status=2)

    def failed(self):
        return self.filter(status=3)
