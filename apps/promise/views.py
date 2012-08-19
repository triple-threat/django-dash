from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View


from promise.forms import NewPromiseForm
from promise.models import Promise, Profile

from util.rediz import get_support_key, get_promise_key, \
    get_ids_from_redis, connection as redis_connection

from event.logging import logger


class Home(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'promises': self.get_promises(),
            'form': NewPromiseForm(),
        }
        return self.render_to_response(context)

    def get_promises(self):
        f = self.request.GET.get('f')
        profile = self.request.user.profile
        promises = Promise.objects.order_by('-id').active()
        if f == 'my':
            return Promise.objects.filter(creator=profile).active()
        elif f == 'sprt':
            return Promise.objects.filter(supporter=profile)
        else:
            return promises


class NewPromise(View):
    """
    Creates a new promise
    """
    def get(self, request):
        return HttpResponseRedirect(reverse('home'))

    def post(self, request):
        form = NewPromiseForm(request.POST)
        if form.is_valid():
            new_promise = form.process(request)
            key = get_promise_key(request.user.profile.id)
            redis_connection.lpush(key, new_promise.id)

            # Logging stuff
            logger.log('promise', data={
                'creator_id': new_promise.creator.id,
                'promise_id': new_promise.id,
            })
        return HttpResponseRedirect(reverse('home'))


class Support(View):

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

        return HttpResponseRedirect(next_url or reverse('home'))

    def update_redis(self, promise_id):
        """
        In Redis, adds this promise to the list of promises that this user supports.
        """
        key = get_support_key(self.request.user.profile.id)
        redis_connection.lpush(key, promise_id)


class PromisePage(TemplateView):
    template_name = 'promise.html'

    def get(self, request, promise_slug):
        context = {
            'app_id': settings.FACEBOOK_APP_ID,
            'promise': Promise.objects.get(slug=promise_slug),
        }
        return self.render_to_response(context)


home = Home.as_view()
new_promise = NewPromise.as_view()
support = Support.as_view()
promise = PromisePage.as_view()
