from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('parts/social.html')
def social(promise, redirect_url=None):
    redirect_url = redirect_url or promise.get_absolute_url()
    blah = promise.creator.get_avatar_url('large', True)
    return {
        'app_id': settings.FACEBOOK_APP_ID,
        'app_name': u'Promise.ly',
        'app_icon': promise.creator.get_avatar_url('large', True),
        'link': promise.get_absolute_url(),
        'post_title': u'Support {}\'s promise'.format(promise.creator.name),
        'post_caption': '',
        'post_description': '"{}"'.format(promise.text),
        'redirect_url': redirect_url,
    }
