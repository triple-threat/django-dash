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

import datetime

from django import forms

from promise.models import Promise


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

DURATION_VALUES = ((x, x) for x in range(1, 7))
DURATION_UNITS = (('days', 'days'), ('weeks', 'weeks'))


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
