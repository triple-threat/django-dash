from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator


from promise.forms import NewPromiseForm, LoginForm
from promise.models import Promise, Profile

from util.rediz import get_support_key, connection as redis_connection


class Home(TemplateView):
    template_name = 'home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'promises': Promise.objects.order_by('-id'),
            'form': NewPromiseForm(),
            'already_supporting': self.get_promises_i_already_support()
        }
        return self.render_to_response(context)

    def get_promises_i_already_support(self):
        """
        Fetches from Redis a list of promise_ids that this user
        already supports.
        """
        key = get_support_key(self.request.user.profile.id)
        return [int(x) for x in redis_connection.lrange(key, 0, -1)]


def new_promise(request):
    """
    Creates a new promise
    """
    if request.POST:
        form = NewPromiseForm(request.POST)
        if form.is_valid():
            form.process(request)
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
        return HttpResponseRedirect(reverse('home'))

    def update_redis(self, promise_id):
        """
        In Redis, adds this promise to the list of promises that this user supports.
        """
        key = get_support_key(self.request.user.profile.id)
        redis_connection.lpush(key, promise_id)


class PromisePage(TemplateView):
    template_name = 'promise.html'


class ProfilePage(TemplateView):
    pass


class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        context = {
            'form': LoginForm(),
        }
        context.update(csrf(request))
        return self.render_to_response(context)


home = Home.as_view()
support = Support.as_view()
profile = ProfilePage.as_view()
promise = PromisePage.as_view()
login = Login.as_view()
