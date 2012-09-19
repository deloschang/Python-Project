from django.conf.urls import patterns, include, url

from webapp.views import index
from django.views.static import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'memeja.views.home', name='home'),
    # url(r'^memeja/', include('memeja.foo.urls')),
    url('^$', index),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
