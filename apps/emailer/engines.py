from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from promise.models import Profile, Promise


class EmailEngine(object):
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
    template = 'emailer/deadline.html'

    def __init__(self, promise_id):
        self.promise = Promise.objects.get(id=promise_id)

    def get_context(self):
        return {
            'promise': self.promise,
        }

    def make_subject_line(self):
        return u"Your promise deadline is almost up!"
