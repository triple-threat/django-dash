import datetime

from django.core.management.base import BaseCommand

from promise.models import Promise

from emailer.engines import DeadlineReminderEngine


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        promises = Promise.objects.all().active()
        for promise in promises:
            if promise.deadline - now < datetime.timedelta(days=1):
                DeadlineReminderEngine(promise.id).send()
