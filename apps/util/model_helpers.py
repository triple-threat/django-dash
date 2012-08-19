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

import random

from django.template.defaultfilters import slugify

from django.contrib.auth.models import User


def make_8_key():
    return User.objects.make_random_password(length=8)


def unique_slugify(obj, base):
    stem = slugify(base)[:140]
    if not stem:
        stem = make_8_key()
    slug = stem
    index = 0
    while True:
        if obj.__class__.objects.filter(slug=slug):
            index += random.randint(1, 100)
            slug = u'{}-{}'.format(stem, index)
        else:
            break
    return slug
