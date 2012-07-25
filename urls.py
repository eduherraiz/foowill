from django.conf.urls.defaults import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse


# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from app.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'', include('app.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

