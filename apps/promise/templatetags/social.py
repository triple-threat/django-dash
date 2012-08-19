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
    redirect_url = redirect_url or promise.get_absolute_url()
    blah = promise.creator.get_avatar_url('large', True)

    if sharer == promise.creator:
        subject = "my"
    else:
        subject = "{}\'s".format(promise.creator.name)

    post_title = u'Support {} promise'.format(subject)

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
