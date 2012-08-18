from django.db import models
from util.model_helpers import unique_slugify


PROMISE_STATUSES = (
    (1, "In Progress"),
    (2, "Succeeded"),
    (3, 'Failed'),
)


class Promise(models.Model):
    text = models.TextField()
    creator = models.ForeignKey('promise.Profile', related_name='creator')
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
    def supporter_count(self):
        return self.supporter.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.text[:20])
        super(Promise, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return unicode(self.user)

