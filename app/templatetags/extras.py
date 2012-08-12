
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
#from django.utils.dateformat import format
from django.utils.translation import ungettext, ugettext
from datetime import datetime, timedelta
#from time import mktime, localtime
import re

register = template.Library()

@register.simple_tag
def add_active(request, name, by_path=False):
    """ Return the string 'active' current request.path is same as name
    
    Keyword aruguments:
    request  -- Django request object
    name     -- name of the url or the actual path
    by_path  -- True if name contains a url instead of url name
    """
    if by_path:
        path = name
    else:
        path = reverse(name)

    if request.path == path:
        return ' active '

    return ''

@register.simple_tag
def parse_tweet(text):
    text = re.sub(r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)', '<a href="\g<0>" rel="external">\g<0></a>', text)
    text = re.sub(r'http://(yfrog|twitpic).com/(?P<id>\w+/?)', '', text)
    text = re.sub(r'#(?P<tag>\w+)', '<a href="http://search.twitter.com/search?tag=\g<tag>" rel="external">#\g<tag></a>', text)
    text = re.sub(r'@(?P<username>\w+)', '@<a href="http://twitter.com/\g<username>/" rel="external">\g<username></a>', text)
    return text
    
    
@register.simple_tag
def tuple2dict(ts):
    ts = settings.__getattr__(ts)
    a = []
    for t in ts:
        a.append(list(t)[0])
    return a
    
@register.simple_tag
def values(ts):
    ts = settings.__getattr__(ts)
    lts = len(ts)
    step = 100/lts
    a = []
    added = 0
    for t in ts:
        a.append(added)
        added = added + step
    a[-1] = 100
    return a
    
def create_time_string(seconds):
    hours = seconds / 3600
    minutes = (seconds % 3600) / 60
    days = hours/24
    weeks = days/7
    months = days/30
    years = months/12
  
    if years > 0:
        return ungettext('a year ago','%(years)d years ago', years) % {'years': years }
        
    if months > 0:
        return ungettext('a month ago','%(months)d months ago', months) % {'months': months }    
    
    if weeks > 0:
        return ungettext('a week ago','%(weeks)d weeks ago', weeks) % {'weeks': weeks }
        
    if days > 0:
        return ungettext('a day ago','%(days)d days ago', days) % {'days': days }
        
    if hours > 0:
        return ungettext('a hour ago','%(hours)d hours ago', hours) % {'hours': hours }
        
    if minutes > 0:
        return ungettext('a minute ago','%(minutes)d minutes ago', minutes) % {'minutes': minutes }
        
    return ugettext('moments ago')
  
@register.filter
def relative_date(data):
    value = datetime.utcnow() - data
    return create_time_string(value.seconds)
    
@register.filter
def relative_date2(data):
    value = data - datetime.utcnow()
    return create_time_string(value.seconds)
