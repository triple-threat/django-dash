from promise.models import Profile

from django.core.management.base import BaseCommand
from util.tasks import refill_redis


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        profiles = Profile.objects.all()
        for prof in profiles:
            refill_redis(prof.id)
