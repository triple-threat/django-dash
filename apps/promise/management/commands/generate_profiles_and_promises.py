import datetime
from random import randint, choice

from promise.models import Profile, Promise
from util.rediz import connection

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        connection.flushdb()

        name_list = [
            "fabio", "lincoln", "suneel", "henry", "vin", "laura", "gabriel",
            "ben", "nytia", "joe", "zach", "adam", "alice", "david", "carl",
            "steve",
        ]

        stuff = [
            "learn to play gitar", "learn to play piano", "workout",
            "code more", "code less", "work less", "work more",
        ]

        for name in name_list:
            try:
                user = User.objects.create_user(username=name, password='promisely')
            except IntegrityError:
                user = User.objects.get(username=name)

            profile = Profile.objects.get(user=user)
            msg = "I, {}, promise that I'll {}"
            stuff_copy = stuff[:]

            for x in range(randint(2, 4)):
                chosen_stuff = choice(stuff_copy)
                stuff_copy.remove(chosen_stuff)
                deadline = datetime.datetime.now() + \
                    datetime.timedelta(days=x + randint(2, 5))

                promise = Promise(
                    text=msg.format(name, chosen_stuff),
                    deadline=deadline,
                    creator=profile
                )
                promise.save()
