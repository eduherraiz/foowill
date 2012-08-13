# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join
from django.utils.translation import ugettext_lazy
from django.utils.translation import string_concat
from datetime import timedelta
import djcelery

try:
    import social_auth
except ImportError:
    import sys
    sys.path.insert(0, "..")
    
import os
import sys
sys.path.append(os.getcwd())

import properties

NAME_PROJECT = "Foowill"

APP_ROOT = getattr(properties, 'app_root', '.')

DEBUG = getattr(properties, 'debug', True)
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': getattr(properties, 'database_engine', 'django.db.backends.sqlite3'),
        'NAME': getattr(properties, 'database_name', 'db.sqlite'),
        'USER': getattr(properties, 'database_user', None),
        'PASSWORD': getattr(properties, 'database_password', ''),
        'HOST': getattr(properties, 'database_host',''),
        'PORT': getattr(properties, 'database_port',''),
        'OPTIONS': {}, #{'autocommit': True,}
    }
}
    
# Django settings for foowill project.
ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)



ADMINS = (
    ('Foowill', 'admin@foowill.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

#Function to prevent a circular import if use  django.utils.translation

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = getattr(properties, 'media_root', '')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = getattr(properties, 'static_root', '')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    getattr(properties, 'app_root', '.')+'/app/static',
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

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@i=d&ra(3&%70=km5bp*+yt)u109-u+#wha7gsa%5hnpoi0t9r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'app.context_processors.debug_mode',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
    join(ROOT_PATH, 'templates_mails')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'django_fields',
    'djsupervisor',
    'gunicorn',
    'social_auth',
    'south',
    'app',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.browserid.BrowserIDBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.contrib.dropbox.DropboxBackend',
    #'social_auth.backends.contrib.flickr.FlickrBackend',
    #'social_auth.backends.contrib.instagram.InstagramBackend',
    #'social_auth.backends.contrib.vkontakte.VkontakteBackend',
    #'social_auth.backends.contrib.skyrock.SkyrockBackend',
    #'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    #'social_auth.backends.OpenIDBackend',
    #'social_auth.backends.contrib.bitbucket.BitbucketBackend',
    #'social_auth.backends.contrib.live.LiveBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY         = 'W5LegvUQ6n8yewTD416XZw'
TWITTER_CONSUMER_SECRET      = 'ibQZkg6Os0UaBr4r4TAJUOfcGYVwljvfKQyNqyrOMCo'
ACCESS_TOKEN                 = '252129698-pPOELRBf9PxPqvrkL05WGbb7MVeo3vtw6JYGb329'
ACCESS_TOKEN_SECRET          = '2NBcrSon1uWdqnWJLj0YPwTJjXvMyTOTtOlCfzCxqE'

LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

BROKER_HOST = "127.0.0.1"
BROKER_BACKEND="redis"
REDIS_PORT=6379
REDIS_HOST = "127.0.0.1"
BROKER_USER = ""
BROKER_PASSWORD =""
BROKER_VHOST = "0"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS=True
CELERY_RESULT_BACKEND='redis'
CELERY_TASK_RESULT_EXPIRES =  10
CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
#CELERY_ALWAYS_EAGER=True
# Disable automatic clean-up of the cropping tool
CROP_AUTO_CLEAN = False
# Let Celery workers import our tasks module
CELERY_IMPORTS = ("tasks", )



CELERYBEAT_SCHEDULE = {
    "Forensic": {
        "task": "tasks.forensic",
        "schedule": timedelta(seconds=60),
        "args": ()
    },
    
    "Killer-Saver": {
        "task": "tasks.killer_saver",
        "schedule": timedelta(seconds=60),
        "args": ()
    },
}


## CACHE

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': 'localhost:6379',
            'OPTIONS': {
                'DB': 1,
            },
        },
    }

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = (60 * 60)
CACHE_MIDDLEWARE_KEY_PREFIX = ''

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location

EMAIL_PROJECT = "info@foowill.com"
ADMIN_EMAIL = "info@foowill.com"
MANDRILL_KEY = "994dcdb3-9fb4-4852-809d-97a7c358a0b4"

hour = ugettext_lazy('hour')
hours = ugettext_lazy('hours')
day = ugettext_lazy('day')
days = ugettext_lazy('days')
week = ugettext_lazy('week')
weeks = ugettext_lazy('weeks')
month = ugettext_lazy('month')
months = ugettext_lazy('months')
year = ugettext_lazy('year')
years = ugettext_lazy('years')
inmediatly = ugettext_lazy('Inmediatly')

ACTIVITY_CHOICES = (
    (600, '10 minutos'),
    (604800, string_concat('1 ', week)),
    (1209600, string_concat('2 ', weeks)),
    (1814400, string_concat('3 ', weeks)),
    (2419200, string_concat('1 ', month)), ##DEFAULT
    (4838400, string_concat('2 ', months)), 
    (7257600, string_concat('3 ', months)),
    (9676800, string_concat('4 ', months)),
    (12096000, string_concat('5 ', months)),
    (14515200, string_concat('6 ', months)),
    (16934400, string_concat('7 ', months)),
    (19353600, string_concat('8 ', months)),
    (21772800, string_concat('9 ', months)),
    (24192000, string_concat('10 ', months)),
    (26611200, string_concat('11 ', months)),
    (29030400, string_concat('1 ', year)),
    (58060800, string_concat('2 ', years)),
    (87091200, string_concat('3 ', years)),
)

PUBLISH_CHOICES = (
    (0, inmediatly), ##DEFAULT
    (3600, string_concat('1 ', hour)),
    (21600, string_concat('6 ', hours)),
    (86400, string_concat('1 ', day)),
    (172800, string_concat('2 ', days)),
    (259200, string_concat('3 ', days)),
    (345600, string_concat('4 ', days)),
    (432000, string_concat('5 ', days)),
    (518400, string_concat('6 ', days)),
    (604800, string_concat('1 ', week)),
    (1209600, string_concat('2 ', weeks)),
    (1814400, string_concat('3 ', weeks)),
    (2419200, string_concat('1 ', month)), ##DEFAULT
    (4838400, string_concat('2 ', months)), 
    (7257600, string_concat('3 ', months)),
    (9676800, string_concat('4 ', months)),
    (12096000, string_concat('5 ', months)),
    (14515200, string_concat('6 ', months)),
    (16934400, string_concat('7 ', months)),
    (19353600, string_concat('8 ', months)),
    (21772800, string_concat('9 ', months)),
    (24192000, string_concat('10 ', months)),
    (26611200, string_concat('11 ', months)),
    (29030400, string_concat('1 ', year)),
    (58060800, string_concat('2 ', years)),
    (87091200, string_concat('3 ', years)),
)


djcelery.setup_loader()

#try:
   #from local_settings import *
#except ImportError, e:
   #pass

#Celery
#python manage.py celeryd -E -B --loglevel=INFO -n w1.hanzo

# Celerymon
#python manage.py celerymon