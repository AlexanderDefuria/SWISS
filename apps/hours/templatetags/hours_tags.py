from django import template
from apps.hours.models import *

register = template.Library()


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

