from django.conf.urls.defaults import patterns, url

from webapp.views import *

urlpatterns = patterns('webapp.views', 
    # temporary url for YC
    url(r'^yc/$', 'yc_no_login'),
    url(r'^yc/(?P<extra>[-\w]+)', 'yc_no_login'),


    #### end ####
    url(r'^$', index, 
                #{'backend' : 'registration.backends.default.DefaultBackend'},
                #### modified for simple activation ####
                {'backend' : 'registration.backends.simple.SimpleBackend'},
                name='webapp_index'),
    url(r'^uncat_library', index_uncat, name='webapp_index_uncat'),
    url(r'^invited/(?P<invitation_key>\w+)/$', 
                #index, {'backend' : 'registration.backends.default.DefaultBackend'},
                #### modified for simple activation ####
                index, {'backend' : 'registration.backends.simple.SimpleBackend'},
                name='invitation_invited'), # change if works
    url(r'^validate/email_duplicates/$', 
                'validate_email_duplicate'),
    url(r'^create/$', create, name='create'),
    url(r'^welcome/hello-world/experience$', helloworld, name='webapp_helloworld'),
    url(r'^welcome/hello-world/create$', helloworld_create, name='webapp_helloworld_create'),
    #url(r'^welcome/hello-world/personalize$', helloworld_generator, name='webapp_helloworld_generator'),
    #url(r'^welcome/hello-world/invite$', helloworld_invite, name='webapp_helloworld_invite'),

    # hardcoded in webapp.views.macromeme_publish for HttpResponse
    (r'^welcome/hello-world/publish/$', 'macromeme_publish'),
    (r'^welcome/hello-world/library/$', 'library'),
    (r'^welcome/hello-world/ohwhy/$', 'fb_privacy_explanation'), 

    url(r'album/from_album_invite/(?P<album_id>\w+)/$',
                from_album_invite,
                name='webapp_from_album_invite'),

    (r'^create/library/$', 'library'),
    (r'^create/publish/$', 'macromeme_publish'),
    (r'^create/remix/(?P<meme_id>\d+)', 'library'),
    (r'^create/ohwhy/$', 'fb_privacy_explanation'),
    url(r'^add_experience/$', add_experience, name='add_experience'),
    url(r'delete/(?P<delete_meme_id>\w+)/$',
                delete_meme,
                name='webapp_delete'),
    url(r'^recreate_map/(?P<meme_id>\w+)/$',
                recreate_map,
                name='webapp_recreate_map'),
    url(r'^add_meme_to_node/$',
                add_meme_to_node,
                name='webapp_add_meme_to_node'),
    url(r'deletealbum/(?P<delete_album_id>\w+)/$',
                delete_album,
                name='webapp_deletealbum'),
    #(r"^(\d+)/$", "show_experience"),
    url(r"^(\d+)/$", 
            show_experience,
            name='webapp_show_experience'),
    (r'^meme_in_album/$', 'meme_in_album'),
    (r'^(?P<linked_username>[-\w]+)/$', 'linked_username'),
    url(r'^thatsrightmax/privatetracking', privatetracking, name='webapp_privatetracking'),
    url(r'^thatsrightmax/userlist', userlist, name='webapp_userlist'),
)
