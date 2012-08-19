import datetime

from django import forms

from promise.models import Promise


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

DURATION_VALUES = ((x, x) for x in range(1, 7))
DURATION_UNITS = (('days', 'days'), ('weeks', 'weeks'))


# class ValidatePromiseForm(forms.Form):
#     promise_id = forms.ModelChoiceField(queryset=Promise.objects.all())
#     result = forms.ChoiceField(PROMISE_STATUSES)

#     def process(self):
#         Promise.objects.filter(id=self.cleaned_data['promise_id']) \
#                 .update(status=self.cleaned_data['result'])
#         return self.cleaned_data['promise_id']


class NewPromiseForm(forms.Form):
    promise_text = forms.CharField()
    duration_value = forms.ChoiceField(DURATION_VALUES)
    duration_unit = forms.ChoiceField(DURATION_UNITS)
    facebook_share = forms.BooleanField(initial=True, required=False)

    def process(self, request):
        timedelta_args = {
            self.cleaned_data['duration_unit']: int(self.cleaned_data['duration_value']),
        }
        deadline = datetime.datetime.now() + datetime.timedelta(**timedelta_args)
        promise = Promise(
            text=self.cleaned_data['promise_text'],
            deadline=deadline,
            creator=request.user.profile,
        )
        promise.save()
        return promise
