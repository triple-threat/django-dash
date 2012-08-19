import functools

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def superuser_required(func):
    """
    Makes sure user has a travelprofile.
    """
    @functools.wraps(func)
    def verify_is_superuser(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    return verify_is_superuser
