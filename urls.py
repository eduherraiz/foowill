from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from app.views import home, config, done, logout, error, form, delete_tweet, contact

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^config/$', config, name='config'),    
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tweet/delete/(?P<id_tweet>(\d+))/$',delete_tweet, name='delete_tweet'),
    url(r'', include('social_auth.urls')),
)