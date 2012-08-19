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

from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('parts/fb.html')
def fb():
    return {
        'app_id': settings.FACEBOOK_APP_ID,
    }


@register.inclusion_tag('parts/social.html')
def social(promise, sharer, redirect_url=None):
    """
    Social sharing template tag
    """
    redirect_url = redirect_url or promise.get_absolute_url()

    if sharer == promise.creator:
        subject = u"I"
    else:
        subject = u"{}".format(promise.creator.name)

    post_title = u'{} made a promise on Promise.ly. Support it!'.format(subject)

    return {
        'app_id': settings.FACEBOOK_APP_ID,
        'app_name': u'Promise.ly',
        'app_icon': promise.creator.get_avatar_url('large', True),
        'link': promise.get_absolute_url(),
        'post_title': post_title,
        'post_caption': '',
        'post_description': '"{}"'.format(promise.text),
        'redirect_url': redirect_url,
    }
