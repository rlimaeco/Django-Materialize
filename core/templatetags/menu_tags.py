import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, pattern_or_urlname):
    """ Return 'active' if `pattern_or_urlname` match the current url

    Useful to set a link's class to 'active' in the menu. 
    """
    try:
        pattern = '^{url}$'.format(url=reverse(pattern_or_urlname))
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
