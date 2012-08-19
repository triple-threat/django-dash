import datetime

from promise.models import Profile, Promise
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        name_list = [
            "fabio", "lincoln", "suneel", "henry", "vin"
        ]
        for name in name_list:
            try:
                user = User.objects.create_user(username=name, password='promisely')
            except IntegrityError:
                user = User.objects.get(username=name)

            try:
                profile = Profile.objects.create(user=user)
            except IntegrityError:
                profile = Profile.objects.get(user=user)

            for x in range(3):
                promise = Promise(
                    text="I, {}, am really excited about this. it's going to be a great promise".format(name),
                    deadline=datetime.datetime.now() + datetime.timedelta(days=x + 2),
                    creator=profile
                )
                promise.save()
