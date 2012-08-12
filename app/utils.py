#-*- coding: UTF-8 -*-
from django.conf import settings
import tweepy
import html2text

def send_email_mandrill(subject, html_content, from_email, from_name, email_to, name_to):
    from mailsnake import MailSnake
    from django.conf import settings

    'Send email using mandrill.com API'
    mapi = MailSnake(settings.MANDRILL_KEY, api='mandrill')
    message={
        'subject':subject, 
        'text': html2text.html2text(html_content),
        'html': html_content,
        'from_email': from_email, 
        'from_name':from_name, 
        'to':[{
            'email':email_to, 
            'name': name_to,
        }]
    }
    mapi.messages.send(message=message) 
    return True
    

def connect_tweepy(user):
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
    access_token = user.tokens["oauth_token"]
    access_token_secret = user.tokens["oauth_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)
