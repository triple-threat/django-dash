from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from promise.views import home, new_promise, support, promise, validate_promise
from analytics.views import metric


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newpromise/', new_promise, name='new_promise'),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^support/(?P<promise_id>[\d]+)/$', support, name="support"),
    url(r'^p/(?P<promise_slug>[a-zA-Z0-9\-_]+)/', promise, name="promise"),
    url(r'^v/(?P<promise_slug>[a-zA-Z0-9\-_]+)/(?P<result>[\d]+)/$', validate_promise, name="validate_promise"),
    url(r'^metric/(?P<metric_name>[a-zA-Z0-9\-_]+)/(?P<hours_ago>[\d]+)/$', metric, name="metric"),
)

# serves the favicon.ico from the root
urlpatterns += patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '{}img/favicon/favicon.ico'.format(settings.STATIC_URL)
    }),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
