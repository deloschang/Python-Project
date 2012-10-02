from django.conf.urls import patterns, include, url

#from webapp.views import index
from django.views.static import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^memeja/', include('memeja.foo.urls')),

    # First page that user comes to 
    url(r'^$', include('webapp.urls')),
    url(r'^', include('registration.backends.default.urls')),


    url(r'^', include('webapp.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    #url(r'^$', registration/registration_form),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
#)
