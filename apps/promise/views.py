from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator

from promise.forms import NewPromiseForm
from promise.models import Promise, Profile

from util.rediz import get_support_key, get_promise_key, \
    get_ids_from_redis, connection as redis_connection

from event.logging import logger


class BasePromiseView(TemplateView):

    @property
    def default_context(self):
        promise_key = get_promise_key(self.request.user.profile.id)
        support_key = get_support_key(self.request.user.profile.id)
        context = {
            'already_supporting': get_ids_from_redis(support_key),
            'my_promises': get_ids_from_redis(promise_key),
        }

        copy = context.copy()
        return copy


class Home(BasePromiseView):
    template_name = 'home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.default_context
        context.update({
            'promises': Promise.objects.order_by('-id').active(),
            'form': NewPromiseForm(),
        })
        return self.render_to_response(context)


def new_promise(request):
    """
    Creates a new promise
    """
    if request.POST:
        form = NewPromiseForm(request.POST)
        if form.is_valid():
            new_promise = form.process(request)
            key = get_promise_key(request.user.profile.id)
            redis_connection.lpush(key, new_promise.id)

            logger.log('promise', data={'creator_id': new_promise.creator.id, 'promise_id': new_promise.id})

    return HttpResponseRedirect(reverse('home'))


class Support(View):
    def get(self, request, promise_id, supporter_id):
        """
        Adds a supporter, making sure not to duplicate.
        """
        promise = Promise.objects.get(id=promise_id)
        supporter = Profile.objects.get(id=supporter_id)
        if supporter != promise.creator and supporter not in promise.supporter.all():
            promise.supporter.add(supporter)
            self.update_redis(promise.id)
            logger.log('support', data={'supporter_id': supporter.id, 'promise_id': promise.id})

        return HttpResponseRedirect(reverse('home'))

    def update_redis(self, promise_id):
        """
        In Redis, adds this promise to the list of promises that this user supports.
        """
        key = get_support_key(self.request.user.profile.id)
        redis_connection.lpush(key, promise_id)


class PromisePage(BasePromiseView):
    template_name = 'promise.html'

    def get(self, request, promise_slug):
        context = self.default_context
        context.update({
            'app_id': settings.FACEBOOK_APP_ID,
            'promise': Promise.objects.get(slug=promise_slug),
        })
        return self.render_to_response(context)


home = Home.as_view()
support = Support.as_view()
promise = PromisePage.as_view()
