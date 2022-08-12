from django import template
from apps.hours.models import *

register = template.Library()


@register.inclusion_tag("entry/components/sidebar.html", takes_context=True)
def get_sidebar(context):
    return {'user': context['user']}


@register.inclusion_tag("entry/components/topbar.html")
def get_topbar(image):
    return {'image': image}


@register.inclusion_tag("entry/components/pill.html")
def get_pill(team):
    return {'team': team}


@register.inclusion_tag("entry/components/pill_link.html")
def get_pill(team, next_page):
    return {
        'team': team,
        'next_page': next_page
    }


@register.inclusion_tag("entry/components/team-link.html")
def get_team_link(team, next_page):
    return {
        'team': team,
        'next_page': next_page
    }


@register.inclusion_tag("entry/components/team-card-select.html")
def get_team_card_select(team, next_page):
    return {
        'team': team,
        'next_page': next_page
    }


@register.filter
def modulo(num, val):
    return str(num // val) + " " + str(num % val)


@register.filter
def get_total_user_hours(request):
    logs = Log.objects.all().filter(status=1)
    if Gremlin.objects.all().contains(user=request.user.id):
        logs = logs.filter(gremlin__user=request.user)

    total_minutes = 0
    for log in logs:
        total_minutes += log.minutes

    return total_minutes

