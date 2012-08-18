from django.db import models


PROMISE_STATUSES = (
    (1, "In Progress"),
    (2, "Succeeded"),
    (3, 'Failed'),
)


class Promise(models.Model):
    text = models.TextField()
    creator = models.ForeignKey('promise.Profile')
    deadline = models.DateTimeField()
    status = models.PositiveSmallIntegerField(choices=PROMISE_STATUSES, default=1)

    def __unicode__(self):
        return u"{}:{}".format(self.text[:15], self.creator)


class Profile(models.Model):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return unicode(self.user)
