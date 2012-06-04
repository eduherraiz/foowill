# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from social_auth.models import UserSocialAuth
from datetime import datetime,timedelta
from django_fields.tests import EncryptedCharField
import twitter
import tweepy

# Define a custom User class to work with django-social-auth
class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    configured = models.BooleanField(default=False)
    user = models.OneToOneField(UserSocialAuth)
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    email = models.EmailField(blank=True)
    
    ACTIVITY_CHOICES = (
      (30, '30 seconds'),
      (120, '2 minutes'),
      (604800, '1 week'),
      (1209600, '2 weeks'),
      (2419200, '1 month'), ##DEFAULT
      (7257600, '3 months'), 
      (14515200, '6 months'),
      (29030400, '1 year')
    )
    #intervalo de periodo de inactividad para considerar al usuario muerto/medio-muerto (segun si email ping o no)
    activity_interval = models.IntegerField(choices=ACTIVITY_CHOICES, default=2419200, blank=True)
    
    PUBLISH_CHOICES = (
      (0, 'Inmediatly'), ##DEFAULT
      (3600, '1 hour'),
      (21600, '6 hour'),
      (86400, '1 day')
    )
    #intervalo de tiempo entre emisiones de tweets una vez muerto
    publish_interval = models.IntegerField(choices=PUBLISH_CHOICES, default=0, blank=True)

    MAIL_CHOICES = (
      (30, '30 seconds'),
      (120, '2 minutes'),
      (604800, '1 week'),
      (1209600, '2 weeks'), ##DEFAULT
      (2419200, '1 month'), 
      (7257600, '3 months'), 
      (14515200, '6 months'),
      (29030400, '1 year')
    )
    #tiempo a esperar desde half-dead hasta dead
    mail_interval = models.IntegerField(choices=MAIL_CHOICES, default=1209600, blank=True)
    
    #fecha de la última publicación en twitter
    last_update = models.DateTimeField(blank=True, null=True)
    
    #fecha para la siguiente comprobación del estado de twitter
    next_check = models.DateTimeField(blank=True, null=True)
    
    #if (now() - last_update) > activity_interval: 
	#half_dead = True
    half_dead = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)

    #if we are waiting for a mail ping
    wait_mail = models.BooleanField(default=False)
    
    #For the ask in the modal
    neverupdate = models.BooleanField(default=False)
    alwaysupdate = models.BooleanField(default=False)
    nottodayupdate = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    def update_date(self):
	"Save the last update date in twitter for the user"
	api = twitter.Api()
	statuses = api.GetUserTimeline(self.username, count=1)
	if len(statuses) > 0:
	    new_date = datetime.utcfromtimestamp(statuses[0].created_at_in_seconds)
	    next_check = new_date + timedelta(seconds=self.activity_interval)
	    if not self.last_update:
		self.last_update = new_date
		self.next_check = next_check
		self.save()
		return True
		
	    if self.last_update < new_date:
		self.last_update = new_date
		self.next_check = next_check
		self.save()
		return True

    def update_twitter_status(self, text):
	if text:
	    # == OAuth Authentication ==
	    #
	    # This mode of authentication is the new preferred way
	    # of authenticating with Twitter.

	    # The consumer keys can be found on your application's Details
	    # page located at https://dev.twitter.com/apps (under "OAuth settings")
	    consumer_key = settings.TWITTER_CONSUMER_KEY
	    consumer_secret= settings.TWITTER_CONSUMER_SECRET

	    # The access tokens can be found on your applications's Details
	    # page located at https://dev.twitter.com/apps (located 
	    # under "Your access token")
	    access_token = self.user.tokens["oauth_token"]
	    access_token_secret = self.user.tokens["oauth_token_secret"]

	    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	    auth.set_access_token(access_token, access_token_secret)

	    api = tweepy.API(auth)

	    # If the authentication was successful, you should
	    # see the name of the account print out

	    # If the application settings are set for "Read and Write" then
	    # this line should tweet out the message to your account's 
	    # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
	    api.update_status(text)

    def show_modal(self):
	if self.alwaysupdate:
	    return False
	if self.neverupdate:
	    return False
	if self.nottodayupdate and (self.nottodayupdate > (datetime.now() - timedelta(days=1))):
	    return False
	return True
	
    def is_authenticated(self):
        return True
        
# Define Tweet 
class Tweet(models.Model):
    text = EncryptedCharField(max_length=140, unique=True)
    user = models.ForeignKey(UserSocialAuth)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    
    def pretty_date(self):
	now = datetime.now()
	diff = now - self.pub_date 
	seconds = diff.seconds
	if diff.days is 0:
	    if seconds < 60:
		return "%ds" % seconds
	    elif seconds < 3600:
		return "%dm" % ((seconds + 60 / 2) / 60)
	    else:
		return "%dh" % ((seconds + 3600 / 2) / 3600)
	else:
	    return "%d/%d/%d" % (self.pub_date.day,self.pub_date.month,self.pub_date.year)

    def __str__(self):
        return self.text
     
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend


def facebook_extra_values(sender, user, response, details, **kwargs):
    return False

pre_update.connect(facebook_extra_values, sender=FacebookBackend)
