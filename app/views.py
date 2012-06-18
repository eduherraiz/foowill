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
    try: 
        instance = UserSocialAuth.objects.filter(provider='twitter',user=userg).get()
    except UserSocialAuth.DoesNotExist:
        return None
    try:
        return CustomUser.objects.filter(user=instance).get()
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create(user=instance, username=userg.username)
        user.update_date()
        user.update_twitter_photo()
        user.save()
        return user

def contact(request):
    if request.user.is_authenticated():
        user = get_user(request.user)
        if not user.configured:
            return HttpResponseRedirect('/config/') # Redirect after POST
    else:
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
        else:
            infomail = "fail"

    else:
        form = ContactForm() # An unbound form
        infomail = {}
        
    ctx = {
        'form': form,
        'tweetform': TweetForm(),
        'user': user,
        'infomail' : infomail,
    }
        
    return render_to_response('contact.html', ctx, RequestContext(request))
        
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        user = get_user(request.user)
        #Initial login have to configure the app -> redirecting
        if not user.configured:
            return HttpResponseRedirect('/config/') # Redirect after POST
    else:
	user = ()
	
    ctx = {
        'tweetform': TweetForm(),
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
            #user.update_twitter_photo() #Not necessary yet, updated on first save
            user.save()
            if not user.configured:
                #user.update_date() #Not necessary yet, updated on first save
                user.configured = True
                user.save()
            saved = True
    else:
        form = ConfigForm(instance=user) # An unbound form
        
    ctx = {
        'form': form,
        'tweetform': TweetForm(),
        'user': user,
        'saved' : saved,
    }
    
    return render_to_response('config.html', ctx, RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    user = get_user(request.user)
    if not user.configured:
        return HttpResponseRedirect('/config/') # Redirect after POST

    new_posttweet = False
    if request.method == 'POST': # If the form has been submitted...
        tweetf = TweetForm(request.POST) # A form bound to the POST data
        if tweetf.is_valid(): # All validation rules pass
            #Save the tweet in the table
            text = tweetf.cleaned_data['text']
            pub_date = datetime.utcnow() 
            
            t = Tweet(text=text, pub_date=pub_date, user=user)
            t.save()
            new_posttweet = user.show_modal_new_tweet()
            if user.alwaysupdate:
                tweet = _("I saved a tweet that will be published when I die with http://foowill.com @foo_will")
                try:
                    user.update_twitter_status(tweet)
                except TweepError:
                    count = Tweet.objects.filter(user=user).count()
                    user.update_twitter_status("%s (%d)" % (tweet, count))
                except:
                    pass
            user.save()
    else:
        tweetf = TweetForm()
        
    tweets = Tweet.objects.filter(user=user).order_by('-pub_date')
    updatetweetform = UpdateTweetForm()
    
    ctx = {
        'tweetform': tweetf,
        'tweets': tweets,
        'user': user,
        'updatetweetform': updatetweetform,
        'new_posttweet': new_posttweet,
    }
    
    return render_to_response('done.html', ctx, RequestContext(request))

    
@login_required
def delete_tweet(request, id_tweet):
    """Delete tweet"""
    user = get_user(request.user)
    try:
        t = Tweet.objects.filter(pk=id_tweet, user=user).get()
        t.delete()
    except:
        pass

    
    return HttpResponseRedirect('/done/') # Redirect after POST

@login_required
def update_status(request):
    """Update user status in her twitter account"""
    user = get_user(request.user)
    sendupdate = False
    #Saving user option for future updates
    if request.method == 'POST': # If the form has been submitted...
        if 'never' in request.POST:
            user.neverupdate = True
            user.save()
        elif 'nottoday' in request.POST:
            user.nottodayupdate = datetime.utcnow()
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
                tweet = form.cleaned_data['updatetweet']
                
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
