import datetime

from django import forms

from models import Promise


class NewPromiseForm(forms.Form):
    text = forms.CharField()
    deadline = forms.DateField(initial=datetime.datetime.today)

    def process(self, request):
        promise = Promise(
            text=self.cleaned_data['text'],
            deadline=self.cleaned_data['deadline'],
            creator=request.user.profile,
        )
        promise.save()
