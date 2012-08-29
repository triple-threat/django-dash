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

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django_facebook.views import connect
from django_facebook.api import get_persistent_graph

from promise.forms import NewPromiseForm
from promise.models import Promise, Profile
from promise.templatetags.social import social

from util.rediz import get_support_key, get_promise_key, connection as redis_connection

from event.logging import logger


class Home(TemplateView):
    """
    Main promise feed
    """
    template_name = 'home.html'
    ajax_template_name = 'ajax_home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'promises': self.get_promises(),
        }
        if request.is_ajax():
            return render(request, self.ajax_template_name, context)
        else:
            context['form'] = NewPromiseForm()
            return self.render_to_response(context)

    def get_promises(self):
        f = self.request.GET.get('f')
        promises = Promise.objects.all().active()
        if self.request.user.is_authenticated():
            profile = self.request.user.profile
            if f == 'my-promises':
                promises = Promise.objects.filter(creator=profile).active()
            elif f == 'supported-by-me':
                promises = Promise.objects.filter(supporter=profile).active()
            elif f == 'my-friends':
                promises = Promise.objects.filter(creator__in=profile.friends(self.request)).active()
        return promises.order_by('-id')


class ValidatePromise(View):
    """
    Creator of a promise verifies whether or not the promise was fulfilled.
    """
    def get(self, request, promise_slug, result):
        try:
            promise = Promise.objects.get(slug=promise_slug)
        except Promise.DoesNotExist:
            pass
        else:
            if request.user.profile == promise.creator:
                promise.status = result
                promise.save()

                # Posting to facebook
                post_data = social(promise, self.request.user.profile)
                msg = (u'I just achieved my promise on Promise.ly: '
                       u'{post_description}. Thanks for your support! {}').format(promise.get_absolute_url())
                self.request.user.profile.wall_post(
                    self.request, msg.format(**post_data))
        return HttpResponseRedirect(reverse('promise', args=[promise_slug]))


class NewPromise(View):
    """
    Creates a new promise
    """
    def dispatch(self, request, *args, **kwargs):
        # We'll have to redirect the user to the facebook oauth
        # flow. Let's store promise data to avoid the need of typing it
        # all over again.
        data = request.POST.copy()
        if data:
            request.session['_delayed_save'] = request.POST.copy()
        return super(NewPromise, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if '_delayed_save' in request.session:
            promise = self.save_promise(request.session.pop('_delayed_save'))
            if promise:
                return HttpResponseRedirect(reverse('promise', args=[promise.slug]))
        return HttpResponseRedirect(reverse('home'))

    @method_decorator(login_required)
    def post(self, request):
        promise = self.save_promise(request.POST)
        if promise:
            return HttpResponseRedirect(reverse('promise', args=[promise.slug]))
        else:
            return HttpResponseRedirect(reverse('home'))

    def save_promise(self, data):
        form = NewPromiseForm(data)
        if form.is_valid():
            new_promise = form.process(self.request)
            key = get_promise_key(self.request.user.profile.id)
            redis_connection.lpush(key, new_promise.id)

            # Posting to facebook
            if data.get('facebook_share') == 'on':
                post_data = social(new_promise, self.request.user.profile)
                msg = (u'I just created a promise on Promise.ly: '
                       u'{post_description}. Please support me! {link}')
                self.request.user.profile.wall_post(
                    self.request, msg.format(**post_data))

            # Logging stuff
            logger.log('promise', data={
                'creator_id': new_promise.creator.id,
                'promise_id': new_promise.id,
            })
            return new_promise


class Support(View):
    """
    This view handles the user action of supporting a promise.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Support, self).dispatch(request, *args, **kwargs)

    def get(self, request, promise_id, next_url=None):
        """
        Adds a supporter, making sure not to duplicate.
        """
        promise = Promise.objects.get(id=promise_id)
        supporter = Profile.objects.get(id=self.request.user.profile.id)
        if supporter != promise.creator and supporter not in promise.supporter.all():
            promise.supporter.add(supporter)
            self.update_redis(promise.id)
            logger.log('support', data={'supporter_id': supporter.id, 'promise_id': promise.id})

            # Posting to facebook
            post_data = {
                'creator_fb_id': promise.creator.facebook_id,
                'link': promise.get_absolute_url()}
            msg = (u'I just supported @[{creator_fb_id}]\'s promise on Promise.ly! '
                   u'Give your support, too. {link}')
            self.request.user.profile.wall_post(
                self.request, msg.format(**post_data))

        return HttpResponseRedirect(next_url or reverse('promise', args=[promise.slug]))

    def update_redis(self, promise_id):
        """
        In Redis, adds this promise to the list of promises that this user supports.
        """
        key = get_support_key(self.request.user.profile.id)
        redis_connection.lpush(key, promise_id)


class PromisePage(TemplateView):
    """
    This view renders the promise landing page.
    """
    template_name = 'promise.html'

    def get(self, request, promise_slug):
        promise = Promise.objects.get(slug=promise_slug)
        context = {
            'app_id': settings.FACEBOOK_APP_ID,
            'promise': promise,
            'supporters_ordered_by_friends': promise.supporters_ordered_by_friends(request),
        }
        return self.render_to_response(context)


@csrf_exempt
def fbconnect(request):
    # Calling the real facebook connect() view
    response = connect(request)
    if not 'facebook_login' in request.REQUEST:
        fbid = get_persistent_graph(request).get('me')['id']
        user = authenticate(facebook_id=fbid)
        login(request, user)
        response.status_code = 302
        response['Location'] = '/'
    return response


home = Home.as_view()
new_promise = NewPromise.as_view()
support = Support.as_view()
promise = PromisePage.as_view()
validate_promise = ValidatePromise.as_view()
