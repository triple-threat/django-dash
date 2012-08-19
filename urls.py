from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from promise.views import home, new_promise, support, profile, promise

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newpromise/', new_promise, name='new_promise'),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^support/(?P<promise_id>[\d]+)/(?:(?P<supporter_id>[\d]+)/)?$', support, name="support"),
    url(r'^profile/(?P<username>[a-zA-Z0-9\-_]+)/', profile, name="profile"),
    url(r'^p/(?P<promise_slug>[a-zA-Z0-9\-_]+)/', promise, name="promise"),
)

# serves the favicon.ico from the root
urlpatterns += patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '{}img/favicon/favicon.ico'.format(settings.STATIC_URL)
    }),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
