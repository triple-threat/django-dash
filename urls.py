from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

from promise.views import home, new_promise, support

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newpromise/', new_promise, name='new_promise'),
    url(r'^support/(?P<promise_id>[\d]+)/(?:(?P<supporter_id>[\d]+)/)?$', support, name="support"),
)

urlpatterns += staticfiles_urlpatterns()
