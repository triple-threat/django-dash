import datetime

from django import forms

from models import Promise


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


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
