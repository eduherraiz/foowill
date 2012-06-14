 #-*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.conf import settings
from django.utils.translation import ugettext as _
from datetime import datetime

from tweepy.error import TweepError

from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.models import UserSocialAuth

from app.models import Tweet, CustomUser
from app.utils import send_email_mandrill
from app.forms import *
import html2text

def get_user(userg):
    instance = UserSocialAuth.objects.filter(provider='twitter',user=userg).get()
    user = None
    try:
        user = CustomUser.objects.filter(user=instance).get()
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create(user=instance, username=userg)
    return user

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        logued = True
        user = get_user(request.user)
    else:
	logued = False
	user = ()
	
    ctx = {
        'logued': logued,
        'user': user,
    }    
    return render_to_response('home.html', ctx, RequestContext(request))

@login_required
def config(request):
    """Login complete view, displays user data"""
    user = get_user(request.user)
    
    saved = False
        
    if request.method == 'POST': # If the form has been submitted...
        form = ConfigForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #Save the user config in the table
            user.username = request.user.username
            user.email = form.cleaned_data['email']
            user.publish_interval = form.cleaned_data['publish_interval']
            user.mail_interval = form.cleaned_data['mail_interval']
            user.activity_interval = form.cleaned_data['activity_interval']
            
            user.save()
            if not user.configured:
                user.update_date()
                user.configured = True
                user.save()
            saved = True
    else:
        form = ConfigForm(instance=user) # An unbound form
        
    ctx = {
        'form': form,
        'user': user,
        'logued' : True, 
        'saved' : saved,
    }
    
    return render_to_response('config.html', ctx, RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    user = get_user(request.user)
    newtweet = False
   
    if request.method == 'POST': # If the form has been submitted...
        form = TweetForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #Save the tweet in the table
            text = form.cleaned_data['text']
            
            t = Tweet(text=text, user=user)
            t.save()
            newtweet = True
            if user.alwaysupdate:
                tweet = _("I saved a tweet that will be published when I die with http://foowill.com @foo_will")
                newtweet = False
                try:
                    user.update_twitter_status(tweet)
                except TweepError:
                    count = Tweet.objects.filter(user=user).count()
                    user.update_twitter_status("%s (%d)" % (tweet, count))
                except:
                    pass
    else:
        form = TweetForm() # An unbound form
        
    tweets = Tweet.objects.filter(user=user).order_by('-pub_date')
    updatetweetform = UpdateTweetForm()
    
    ctx = {
        'form': form,
        'tweets': tweets,
        'user': user,
        'logued': True,
        'newtweet': newtweet,
        'updatetweetform': updatetweetform,
    }
    
    return render_to_response('done.html', ctx, RequestContext(request))
    
@login_required
def delete_tweet(request, id_tweet):
    """Delete tweet"""
    user = get_user(request.user)
   
    t = Tweet.objects.filter(pk=id_tweet, user=user).get()
    t.delete()
    
    return HttpResponseRedirect('/done/') # Redirect after POST

@login_required
def updatestatus(request):
    """Update user status in her twitter account"""
    user = get_user(request.user)
    sendupdate = False
    #Saving user option for future updates
    if request.method == 'POST': # If the form has been submitted...
        if 'never' in request.POST:
            user.neverupdate = True
            user.save()
        elif 'nottoday' in request.POST:
            user.nottodayupdate = datetime.now()
            user.save()
        elif 'ever' in request.POST:
            user.alwaysupdate = True
            user.save()
            sendupdate = True
        elif 'now' in request.POST:
            sendupdate = True

        if sendupdate:
            form = UpdateTweetForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                #Send the tweet to twitter
                tweet = form.cleaned_data['tweet']
                
                try:
                    user.update_twitter_status(tweet)
                except TweepError:
                    try:
                        count = Tweet.objects.filter(user=user).count()
                        user.update_twitter_status("%s (%d)" % (tweet, count))
                    except:
                        pass
  
    return HttpResponseRedirect('/done/') # Redirect after POST
    
    
def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', {}, RequestContext(request))


def contact(request):
    if request.user.is_authenticated():
        user = get_user(request.user)
        logued = True
    else:
        logued = False
        user = ()

    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #Send the email
            subject = form.cleaned_data['subject']
            html_content = form.cleaned_data['message']
            text_content = html2text.html2text(html_content)
            from_email = form.cleaned_data['sender']
            from_name = form.cleaned_data['name']
            info = send_email_mandrill(subject, text_content, html_content, from_email, from_name, settings.ADMIN_EMAIL, 'Admin foowill')
            infomail = info[0]
            
            #user = CustomUser.objects.filter(username=request.user).get()
            #return HttpResponseRedirect('/contact') # Redirect after POST
    else:
        infomail = {}
        form = ContactForm() # An unbound form
        
    ctx = {
        'form': form,
        'user': user,
        'logued': logued,
        'infomail' : infomail,
    }
        
    return render_to_response('contact.html', ctx, RequestContext(request))