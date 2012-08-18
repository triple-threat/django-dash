from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView, View

from promise.forms import NewPromiseForm
from promise.models import Promise


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'promises': Promise.objects.order_by('-id'),
            'form': NewPromiseForm()
        }
        return self.render_to_response(context)


def new_promise(request):
    if request.POST:
        form = NewPromiseForm(request.POST)
        if form.is_valid():
            form.process(request)
    return HttpResponseRedirect(reverse('home'))


home = Home.as_view()
