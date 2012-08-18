from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView, View

from promise.forms import NewPromiseForm
from promise.models import Promise, Profile

from util.rediz import get_support_key, connection as redis_connection


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'promises': Promise.objects.order_by('-id'),
            'form': NewPromiseForm(),
            'already_supporting': self.get_my_supported()
        }
        return self.render_to_response(context)

    def get_my_supported(self):
        conn = redis_connection.get_connection()
        key = get_support_key(self.request.user.profile.id)
        return [int(x) for x in conn.lrange(key, 0, -1)]


def new_promise(request):
    if request.POST:
        form = NewPromiseForm(request.POST)
        if form.is_valid():
            form.process(request)
    return HttpResponseRedirect(reverse('home'))


class Support(View):
    def get(self, request, promise_id, supporter_id):
        promise = Promise.objects.get(id=promise_id)
        supporter = Profile.objects.get(id=supporter_id)
        if supporter != promise.creator and supporter not in promise.supporter.all():
            promise.supporter.add(supporter)
            self.update_redis(promise.id)
        return HttpResponseRedirect(reverse('home'))

    def update_redis(self, promise_id):
        conn = redis_connection.get_connection()
        key = get_support_key(self.request.user.profile.id)
        conn.lpush(key, promise_id)


home = Home.as_view()
support = Support.as_view()
