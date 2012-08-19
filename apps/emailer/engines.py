from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from promise.models import Profile, Promise


class EmailEngine(object):

    from_address = "Promise.ly <notifications@promise.ly>"

    def render(self):
        return render_to_string(self.template, self.get_context())

    def send(self):
        message = EmailMessage(
            self.make_subject_line(),
            self.render(),
            self.from_address,
            self.get_recipients(),
            headers={'Reply-To': self.from_address}
        )
        message.content_subtype = "html"
        message.send()


class NewSupporterEngine(EmailEngine):

    template = 'emailer/new_supporter.html'

    def __init__(self, supporter_id, promise_id):
        self.supporter = Profile.objects.get(id=supporter_id)
        self.promise = Promise.objects.get(id=promise_id)

    def get_recipients(self):
        return [self.promise.creator.user.email]

    def get_context(self):
        return {
            'supporter': self.supporter,
            'promise': self.promise,
        }

    def make_subject_line(self):
        return u"You have a new supporter!"
