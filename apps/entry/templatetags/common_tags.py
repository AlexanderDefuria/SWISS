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


@register.simple_tag
def get_match_fields():
    print([f.name for f in Match._meta.get_fields()])
    return [f.name for f in Match._meta.get_fields()]


@register.filter
def get_pit_info(team, field):
    try:
        return Pits.objects.filter(team_id=team.id)[0].__getattribute__(field)
    except IndexError:
        return "NA"

# {% for team in team_list %}
#     {{ team|get_pit_info:"weight" }}
# {% endfor %}


