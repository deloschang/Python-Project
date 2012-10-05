from django.conf.urls.defaults import patterns, url

from webapp.views import *

urlpatterns = patterns('webapp.views', 
    url(r'^$', index, {'backend' : 'registration.backends.default.DefaultBackend'}, name='memeja_index'),
    url(r'^create/$', create, name='create'),
    url(r'^add_experience/$', add_experience, name='add_experience'),
    
    (r"^(\d+)/$", "show_experience"),
)
