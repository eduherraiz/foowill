 #-*- coding: UTF-8 -*-
from django.forms import ModelForm, Textarea, Form, CharField, EmailField
from app.models import Tweet, CustomUser

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 5} ),
        }	

class ConfigForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','activity_interval', 'publish_interval', 'mail_interval', )
        #widgets = {
            #'text': Textarea(attrs={'cols': 40, 'rows': 5}),
        #}	 
 
class ContactForm(Form):
    subject = CharField(max_length=200)
    message = CharField(widget=Textarea(attrs={'cols': 80, 'rows': 5}) )
    sender = EmailField(label="Your email address")
    #cc_myself = forms.BooleanField(required=False)
    
class UpdateTweetForm(Form):
    tweet = CharField(required=True, max_length=140, widget=Textarea(attrs={'cols': 80, 'rows': 5}), initial="He guardado un tweet que podrás leer cuando muera gracias a http://foowill.com @foo_will")
