from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('social.html')
def social(promise, redirect_url=None):
    redirect_url = redirect_url or promise.get_absolute_url()
    picture = 'https://graph.facebook.com/{}/picture'.format(
        promise.creator.facebook_id) if promise.creator.facebook_id else ''
    return {
        'app_id': settings.FACEBOOK_APP_ID,
        'app_name': u'Promise.ly',
        'app_icon': picture,
        'link': promise.get_absolute_url(),
        'post_title': u'Support {}\'s promise'.format(promise.creator.name),
        'post_caption': '',
        'post_description': '"{}"'.format(promise.text),
        'redirect_url': redirect_url,
    }
