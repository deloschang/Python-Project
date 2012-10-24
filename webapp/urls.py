from django.conf.urls.defaults import patterns, url

from webapp.views import *

urlpatterns = patterns('webapp.views', 
    url(r'^$', index, {'backend' : 'registration.backends.default.DefaultBackend'},
                name='webapp_index'),
    url(r'^invited/(?P<invitation_key>\w+)/$', 
                index, {'backend' : 'registration.backends.default.DefaultBackend'},
                name='invitation_invited'), # change if works
    url(r'^create/$', create, name='create'),
    (r'^create/library/$', 'library'),
    (r'^create/publish/$', 'macromeme_publish'),
    (r'^create/remix/(?P<meme_id>\d+)', 'library'),
    (r'^create/ohwhy/$', 'fb_privacy_explanation'),
    url(r'^add_experience/$', add_experience, name='add_experience'),
    url(r'delete/(?P<delete_meme_id>\w+)/$',
                delete_meme,
                name='webapp_delete'),
    url(r'deletealbum/(?P<delete_album_id>\w+)/$',
                delete_album,
                name='webapp_deletealbum'),
    (r"^(\d+)/$", "show_experience"),
    (r'^meme_in_album/$', 'meme_in_album'),
    (r'^(?P<linked_username>[-\w]+)/$', 'linked_username'),
)
