import datetime

from django.core.management.base import BaseCommand

from promise.models import Promise

from emailer.engines import DeadlineReminderEngine
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        day_ago = now < datetime.timedelta(days=1)
        day_ago = day_ago.replace(tzinfo=timezone.utc)
        promises = Promise.objects.all().active()
        for promise in promises:
            naive_date = promise.deadline

            if naive_date - day_ago:
                DeadlineReminderEngine(promise.id).send()
