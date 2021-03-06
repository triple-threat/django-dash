# Promise.ly -- social commitment platform
#
# Copyright (C) 2012  Promise.ly authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from promise.models import Profile, Promise


class EmailEngine(object):
    """
    Base email engine for rendering a template and sending it.
    """
    from_address = "Promise.ly <notifications@promise.ly>"

    def render(self):
        return render_to_string(self.template, self.get_context())

    def send(self):
        recipients = self.get_recipients()
        # Safety check for sometimes unclean data (no email in User)
        if not recipients or not ''.join(recipients):
            return

        message = EmailMessage(
            self.make_subject_line(),
            self.render(),
            self.from_address,
            recipients,
            headers={'Reply-To': self.from_address}
        )
        message.content_subtype = "html"
        message.send()

    def get_recipients(self):
        return [self.promise.creator.user.email]


class NewSupporterEngine(EmailEngine):
    """
    Email Engine for notifying a user that his/her promise was supported.
    """
    template = 'emailer/new_supporter.html'

    def __init__(self, supporter_id, promise_id):
        self.supporter = Profile.objects.get(id=supporter_id)
        self.promise = Promise.objects.get(id=promise_id)

    def get_context(self):
        return {
            'supporter': self.supporter,
            'promise': self.promise,
        }

    def make_subject_line(self):
        return u"You have a new supporter!"


class DeadlineReminderEngine(EmailEngine):
    """
    Email Engine for notifying a user that his/her promise's deadline is about to arrive.
    """
    template = 'emailer/deadline.html'

    def __init__(self, promise_id):
        self.promise = Promise.objects.get(id=promise_id)

    def get_context(self):
        return {
            'promise': self.promise,
        }

    def make_subject_line(self):
        return u"Your promise deadline is almost up!"
