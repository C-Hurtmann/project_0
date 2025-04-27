from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    request = context['request']
    current_url_name = resolve(request.path).url_name
    return 'active' if current_url_name == url_name else ''
