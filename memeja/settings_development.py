# settings used for local development
from settings_local import * 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

GOOGLE_ANALYTICS_KEY = 'UA-32708243-1'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/Users/deloschang/memeja/webapp/static/media/'
MEDIA_ROOT = '/Users/deloschang/memeja/webapp/static/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"

# be careful changing this - views are hardcoded
MEDIA_URL = '/static/media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"

# be careful changing this - views are hardcoded
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/Users/deloschang/memeja/webapp/static/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp', # main application
    'registration', # registration system
    'invitation', # invitation system
    'south',
    'email_usernames',
    'ajax_select',
    'endless_pagination',
    'social_auth',
    'facepy',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'email_usernames.backends.EmailOrUsernameModelBackend',
    'social_auth.backends.facebook.FacebookBackend', # social_auth
    'social_auth.backends.facebook2.FacebookBackend', # social_auth for extended permissions
    'django.contrib.auth.backends.ModelBackend', # social_auth
)


# social auth keys
FACEBOOK_APP_ID              = '479174175436255'
FACEBOOK_API_SECRET          = 'a0522ed8310df87c00ade91df0352cc8'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_education_history', 'user_photos', 'friends_photos']
# second step for permission when inviting
FACEBOOK_EXTENDED_PERMISSIONS_SECONDSTEP = ['email', 'user_education_history', 'user_photos', 'friends_photos', 'publish_stream']

LOGIN_URL          = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/welcome/hello-world/experience' 
LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

# end



AUTH_PROFILE_MODULE = 'webapp.UserProfile'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'memeja.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'memeja.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/Users/deloschang/memeja/webapp/templates'
)

# Channels and models for ajax-select application
AJAX_LOOKUP_CHANNELS = {
    # simplest way, automatically construct a search channel by passing a dictionary
    #'label'  : {'model':'webapp.Meme', 'search_field':'title'},
    #'invite_user' : {'model':'django.contrib.auth.User'

    # Custom channels are specified with a tuple
    # channel: ( module.where_lookup_is, ClassNameOfLookup )
    'label' : ('webapp.lookups', 'UserLookup'),
    #'person' : ('example.lookups', 'PersonLookup'),
    #'group'  : ('example.lookups', 'GroupLookup'),
    #'song'   : ('example.lookups', 'SongLookup'),
    #'cliche' : ('example.lookups','ClicheLookup')
}

AJAX_SELECT_BOOTSTRAP = True

AJAX_SELECT_INLINES = 'inline'

# Registration Options
ACCOUNT_ACTIVATION_DAYS=20

# Invitation Keys
INVITE_MODE = True
ACCOUNT_INVITATION_DAYS=7  # number of days invitation keys remain valid
INVITATIONS_PER_USER = 99 



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SCHOOL_UCB_ALBUM = 'UCB'
SCHOOL_DARTMOUTH_ALBUM = 'Dartmouth'
YCOMBINATOR = 'YCombinator'
GENERAL = 'General'
