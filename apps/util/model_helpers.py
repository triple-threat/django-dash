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
