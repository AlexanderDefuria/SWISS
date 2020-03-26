from django import template
from apps.entry.models import *
from apps import config

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val == 0


@register.simple_tag
def get_current_event():
    return Event.objects.filter(FIRST_key=config.get_current_event_key())[0]


@register.simple_tag
def get_current_event_id():
    return config.get_current_event_key()

