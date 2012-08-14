 #-*- coding: UTF-8 -*-
from django.forms import ModelForm, Textarea, Form, CharField, EmailField
from app.models import Tweet, CustomUser
from django.utils.translation import ugettext_lazy as _

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('text', )
        widgets = {
            'text': Textarea(),
        }

class ConfigForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','activity_interval', 'publish_interval', 'mail_interval', 'timezone' )
        #widgets = {
            #'text': Textarea(attrs={'cols': 40, 'rows': 5}),
        #}	 
 
class ContactForm(Form):
    subject = CharField(label=_("Message subject"),max_length=200,required=True)
    message = CharField(label=_("Your message"),widget=Textarea(),required=True )
    sender = EmailField(label=_("Email address"), required=True)
    name = CharField(label=_("Your name or company"),max_length=200,required=True)
    #cc_myself = forms.BooleanField(required=False)
    
class UpdateTweetForm(Form):
    updatetweet = CharField(
            required=True, 
            max_length=140, 
            widget=Textarea(), 
            initial=_("I saved a tweet that will be published when I die with http://foowill.com @foo_will"))
