# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from social_auth.models import UserSocialAuth
from datetime import datetime,timedelta
from django_fields.tests import EncryptedCharField
from django.core.mail import EmailMultiAlternatives

from app.utils import send_email_mandrill, connect_tweepy

import twitter
import tweepy

#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Define a custom User class to work with django-social-auth
class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    configured = models.BooleanField(default=False)
    user = models.OneToOneField(UserSocialAuth)
    username = models.CharField(max_length=128)
    photo = models.URLField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    email = models.EmailField(blank=True)

    #intervalo de periodo de inactividad para considerar al usuario muerto/medio-muerto (segun si email ping o no)
    activity_interval = models.IntegerField(choices=settings.ACTIVITY_CHOICES, default=2419200, blank=False)
    
    #intervalo de tiempo entre emisiones de tweets una vez muerto
    publish_interval = models.IntegerField(choices=settings.PUBLISH_CHOICES, default=0, blank=True)

    #tiempo a esperar desde half-dead hasta dead
    mail_interval = models.IntegerField(choices=settings.ACTIVITY_CHOICES, default=1209600, blank=False)
    
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
    
    new_posttweet = models.BooleanField(default=False)
    
    #For the ask in the modal
    neverupdate = models.BooleanField(default=False)
    alwaysupdate = models.BooleanField(default=False)
    nottodayupdate = models.DateTimeField(blank=True, null=True)

    
    objects = CustomUserManager()
    
    #def save(self, *args, **kwargs):
        #if not self.pk:
            #if not self.last_update:
                #self.update_date()
            #if not self.photo:
                #self.update_twitter_photo()
        #super(CustomUser, self).save(*args, **kwargs)
        

    def update_date(self):
	"Save the last update date in twitter for the user"
        api = twitter.Api()
        statuses = api.GetUserTimeline(self.username, count=1)
        if len(statuses) > 0:
            new_date = datetime.utcfromtimestamp(statuses[0].created_at_in_seconds)
            next_check = new_date + timedelta(seconds=self.activity_interval)
        if not self.last_update or (self.last_update < new_date):
            self.last_update = new_date
            self.next_check = next_check
            #self.save()
        return self.last_update

    def update_twitter_status(self, text):
	if text:
            api = connect_tweepy(self.user)
	    api.update_status(text)

    def update_twitter_photo(self):
        api = connect_tweepy(self.user)
        user = api.get_user(self.username)
        self.photo = user.profile_image_url
        #self.save()
	    
    def get_twitter_friends(self):
        api = connect_tweepy(self.user)
        friends =[]
        for friend in tweepy.Cursor(api.friends).items():
            friends.append(friend.screen_name)
        return friends
        

    def show_modal_new_tweet(self):
	if self.alwaysupdate:
	    return False
	if self.neverupdate:
	    return False
	if self.nottodayupdate and (self.nottodayupdate > (datetime.utcnow() - timedelta(days=1))):
	    return False
	return True
	
    def send_email(self, subject, text_content, html_content):
        send_email_mandrill(subject, text_content, html_content, self.email. self.username)


    def send_email_halfdead(self):
	subject = "¿Sigues vivo?"
	text_content = "Get text from template/text_halfdead.txt"
	html_content = "Get <b>html</b> from template/text_halfdead.html"
	self.send_email(subject, text_content, html_content)
	
    def is_authenticated(self):
        return True
        
# Define Tweet 
class Tweet(models.Model):
    text = EncryptedCharField(max_length=140, unique=True)
    user = models.ForeignKey(CustomUser)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.text

#@receiver(post_save, sender=CustomUser)
#def init_user(sender, instance, created, **kwargs):
    #"""Create a matching profile whenever a user object is created."""
    #if created: 
        #instance.update_twitter_photo()
        #instance.update_date()
        ##profile, new = UserProfile.objects.get_or_create(user=instance)

        
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend


def facebook_extra_values(sender, user, response, details, **kwargs):
    return False

pre_update.connect(facebook_extra_values, sender=FacebookBackend)
