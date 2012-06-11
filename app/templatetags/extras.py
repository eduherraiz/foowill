from django import template
from django.core.urlresolvers import reverse
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