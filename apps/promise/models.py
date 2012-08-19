import datetime

from django.db import models
from util.model_helpers import unique_slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_facebook.models import FacebookProfileModel
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe


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
    def supporter_list(self):
        return self.supporter.all()

    @property
    def facebook_url(self):
        return u'https://www.facebook.com/sharer.php?u={}&amp;t={}'.format(
            urlencode(self.full_url), urlencode(u"Support {}'s promise: self.text".format(self.creator)))

    @property
    def twitter_url(self):
        return u'http://twitter.com/?status={}'.format(
            self.tweet_text)

    @property
    def mailto_url(self):

        body = unicode("'{}' - {}").format(self.text, self.creator) + unicode("\n{}").format(urlencode(self.full_url))
        subject = u"Support {}!".format(self.creator)

        res = u'mailto:&#63;body={}&subject={}'.format(urlencode(body), urlencode(subject))
        return mark_safe(res)

    @property
    def tweet_text(self):
        return u"Support {}'s promise! '{}' - {}".format(self.creator.facebook_name or self.creator, self.text, self.full_url)

    @property
    def full_url(self):
        return unicode("http://promise.ly/promise/{}").format(self.slug)

    @property
    def supporter_count(self):
        return self.supporter.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.text[:20])
        super(Promise, self).save(*args, **kwargs)


class Profile(FacebookProfileModel):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return unicode(self.user)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
