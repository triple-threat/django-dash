from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_facebook.api import get_persistent_graph
from django_facebook.models import FacebookProfileModel
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

from util import url_with_domain
from util.model_helpers import unique_slugify
from util.rediz import get_support_key, get_promise_key, get_ids_from_redis

from promise.managers import PromiseManager


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

    objects = PromiseManager()

    def __unicode__(self):
        return u"{}:{}".format(self.text[:15], self.creator)

    @property
    def active(self):
        return self.status == 1

    @property
    def success(self):
        return self.status == 2

    @property
    def supporters(self):
        maxsupporters = 5
        count = self.supporter.count()
        if count > maxsupporters:
            supporters = self.supporter.all()[:maxsupporters]
            return u'{} and {} others support this'.format(
                ', '.join(unicode(i) for i in supporters), count - maxsupporters)
        return ", ".join(unicode(i) for i in self.supporter.all())

    @property
    def mailto_url(self):
        body = u"'{}' - {}".format(self.text, self.creator) + \
            u"\n{}".format(urlencode(self.get_absolute_url()))
        subject = u"Support {}!".format(self.creator)
        res = u'mailto:&#63;body={}&subject={}'.format(urlencode(body), urlencode(subject))
        return mark_safe(res)

    def get_absolute_url(self):
        return url_with_domain(reverse('promise', args=(self.slug,)))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.text[:20])
        super(Promise, self).save(*args, **kwargs)


class Profile(FacebookProfileModel):
    user = models.OneToOneField('auth.User')

    @property
    def name(self):
        return self.facebook_name or unicode(self)

    def get_avatar_url(self, size, local=False):
        convert = {
            'large': '180/200',
            'square': '50/50',
        }

        if local and bool(self.image):
            return url_with_domain(self.image.url)
        return u'https://graph.facebook.com/{}/picture?type={}'.format(
            self.facebook_id, size) if self.facebook_id \
            else 'http://placekitten.com/g/{}'.format(convert.get(size))

    def friends(self, request):
        fb = get_persistent_graph(request)

        # TODO: iterate over the pagination info
        fbids = [int(i['id']) for i in fb.get('me/friends').get('data')]

        return Profile.objects.filter(id__in=fbids)

    @property
    def avatar_square(self):
        return self.get_avatar_url('square')

    @property
    def avatar(self):
        return self.get_avatar_url('large')

    def __unicode__(self):
        return unicode(self.user)


class PromiseUserState(object):
    """Namespace to store status that relates an user to a promise.

    It's used to decide which widget should be shown to the user when
    accessing the promise page or the promise feed. All Anonymous users
    should be marked as "NOTHING".

    Namespaces are one honking great idea -- let's do more of those!
    """
    OWNER = 0
    SUPPORTER = 1
    NOTHING = 2

    @staticmethod
    def from_string(state):
        return getattr(PromiseUserState, state.upper())


def user_promise_state(user, promise):
    """Returns the status between the promise and the currently logged
    in (or anonymous) user. Just a helper to avoid ifs/elifs to
    proliferate in our codebase.
    """

    # We got an anonymous user here, he obviously can't support
    # anything. Let's give him a chance to show the "support this"
    # button.
    if user.is_anonymous():
        return PromiseUserState.NOTHING

    # For owners
    promise_key = get_promise_key(user.profile.id)
    if promise.id in get_ids_from_redis(promise_key):
        return PromiseUserState.OWNER

    # For supporters
    support_key = get_support_key(user.profile.id)
    if promise.id in get_ids_from_redis(support_key):
        return PromiseUserState.SUPPORTER

    return PromiseUserState.NOTHING


def create_profile(sender, instance, created, **kwargs):
    if created:
        from event.logging import logger
        Profile.objects.create(user=instance)
        logger.log('signup')
post_save.connect(create_profile, sender=User)
