from django.conf.urls.defaults import patterns, url

from webapp.views import *

urlpatterns = patterns('webapp.views', 
    url(r'^$', index, {'backend' : 'registration.backends.default.DefaultBackend'}, name='registration.views.register'),
    url(r'^list/$', 'list', name='list'),
)
