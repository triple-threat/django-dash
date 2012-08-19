from django.db import models


class PromiseManager(models.Manager):

    def get_query_set(self):
        return PromiseQuerySet(self.model)


class PromiseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1)

    def expired(self):
        return self.filter(status__in=[2, 3])

    def successful(self):
        return self.filter(status=2)

    def failed(self):
        return self.filter(status=3)
