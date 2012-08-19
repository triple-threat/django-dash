import datetime

from django.core.management.base import BaseCommand

from promise.models import Promise


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        promises = Promise.objects.all().active()
        promises.filter(deadline__lt=now).update(status=3)
