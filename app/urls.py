from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _


# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from app.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^config/$', config, name='config'),    
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^update_status/$', update_status, name='update_status'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^tweet/add/$',add_tweet, name='add_tweet'),
    url(r'^tweet/delete/(?P<id_tweet>(\d+))/$',delete_tweet, name='delete_tweet'),
)