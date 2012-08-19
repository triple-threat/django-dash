import datetime

from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django_facebook.models import FacebookProfileModel
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

from util.model_helpers import unique_slugify


PROMISE_STATUSES = (
    (1, "In Progress"),
    (2, "Succeeded"),
    (3, 'Failed'),
)


class Promise(models.Model):
    text = models.TextField()
    creator = models.ForeignKey('promise.Profile', related_name='creator')
    created = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    status = models.PositiveSmallIntegerField(choices=PROMISE_STATUSES, default=1)
    supporter = models.ManyToManyField('promise.Profile', blank=True, related_name='supporter')
    slug = models.SlugField(unique=True, blank=True)

    def __unicode__(self):
        return u"{}:{}".format(self.text[:15], self.creator)

    @property
    def supporters(self):
        return ",".join([unicode(supporter) for supporter in self.supporter.all()])

    @property
    def mailto_url(self):
        body = unicode("'{}' - {}").format(self.text, self.creator) + unicode("\n{}").format(urlencode(self.full_url))
        subject = u"Support {}!".format(self.creator)
        res = u'mailto:&#63;body={}&subject={}'.format(urlencode(body), urlencode(subject))
        return mark_safe(res)

    def get_absolute_url(self):
        domain = Site.objects.get_current().domain
        path = reverse('promise', args=(self.slug,))
        return u'{}{}'.format(domain, path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.text[:20])
        super(Promise, self).save(*args, **kwargs)


class Profile(FacebookProfileModel):
    user = models.OneToOneField('auth.User')

    @property
    def name(self):
        return self.facebook_name or unicode(self)

    def _get_avatar_url(self, size):
        convert = {
            'large': '180/200',
            'square': '50/50',
        }
        return u'https://graph.facebook.com/{}/picture?type={}'.format(
            self.facebook_id, size) if self.facebook_id \
            else 'http://placekitten.com/g/{}'.format(convert.get(size))

    @property
    def avatar_square(self):
        return self._get_avatar_url('square')

    @property
    def avatar(self):
        return self._get_avatar_url('large')

    def __unicode__(self):
        return unicode(self.user)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
