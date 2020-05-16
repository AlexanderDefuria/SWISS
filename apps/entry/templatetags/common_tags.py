import datetime
import inspect

from django import template
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone

from apps.entry.models import *
from apps import config
import json
from django.conf import settings

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


@register.simple_tag
def get_all_logged_in_users(*args):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    time = timezone.now()
    uid_list = []
    count = 0

    # Build a list of user ids from that query that have last refreshed
    # their expiry date within the last 2:30 minutes to ensure and accurate count
    for session in sessions:
        timediff = session.expire_date - time - datetime.timedelta(days=13, hours=23, minutes=57, seconds=30)
        if datetime.timedelta(seconds=0) < timediff:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
            count += 1

    # Query all logged in users based on id list and return the length of that queryset
    if "unique" in args:
        return len(User.objects.filter(id__in=uid_list))
    else:
        return count


@register.simple_tag
def get_info(team, field, *args):
    try:
        model = Pits
        if "match" in args:
            model = Match

        if len(model.objects.filter(team_id=team, event_id=config.get_current_event_id())) == 0:
            return "No Data"

        if "dependant" in args:
            return dependant(team, field, model, args)
        elif "average" in args:
            return get_average(team, field, model)
        elif "total" in args:
            return get_total(team, field, model)
        elif "list" in args:
            return get_list(team, field, model)
        elif "possible" in args:
            return get_possible(team, field, model)

        return "ERROR"

    except IndexError:
        return "NA"


def get_average(team, field, model):
    if model.objects.first()._meta.get_field(field).get_internal_type() not in ('IntegerField', 'SmallIntegerField', 'BooleanField'):
        result_list = get_list(team, field, model)
        most_common = 'None'
        occured = 0
        for each in result_list:
            if result_list.count(each) > occured:
                occured = result_list.count(each)
                most_common = each

        # print(str(most_common) + " occured " + str(occured) + " times.")

        return most_common

    return round(1000 * (get_total(team, field, model) / len(model.objects.filter(team_id=team.id)))) / 1000


def get_total(team, field, model):
    total = 0
    object_list = model.objects.filter(team_id=team.id)
    boolean = model.objects.first()._meta.get_field(field).get_internal_type() == 'BooleanField'

    for entry in object_list:
        if boolean:
            # print(entry.__getattribute__(field))
            if entry.__getattribute__(field):
                total += 1
        else:
            total += entry.__getattribute__(field)

    return total


def get_list(team, field, model):
    object_list = model.objects.filter(team_id=team.id)
    result_list = []
    return_list = {}

    for entry in object_list:
        result_list.append(entry.__getattribute__(field))

    if inspect.stack()[1].function == 'get_info':  # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
        for each in result_list:
            if return_list.get(each) is None:
                return_list[each] = 1
            else:
                return_list[each] += 1

        d = return_list
        return_list = {}
        for k in sorted(d, key=d.get, reverse=True):
            # print(k, d[k])
            rename = []
            if field == 'tele_positions':
                rename = ["Against Power Port", "Initiation Line Area", "Trench Run", "Behind Control Panel"]
            elif field == 'field_timeout_pos':
                rename = ["Nothing", "Parked", "Attempted Climb", "Successful Climb"]

            if rename is not []:
                return_list[rename[k]] = d[k]
            else:
                return_list[k] = d[k]

        return list(return_list)

    else:
        return result_list


def get_possible(team, field, model):
    object_list = model.objects.filter(team_id=team.id)
    default = model._meta.get_field(field).default

    # print("DEFAULT: " + str(default))

    for each in object_list:
        if each.__getattribute__(field) != default:
            return "Yes"

    return "No"


def dependant(team, field, model, args):
    dependant_arg = ''
    for arg in args:
        if "dependant-" in str(arg):
            dependant_arg = str(arg)[10:]
            continue
        if args.index(arg) == len(args) - 1:
            return 0

    object_list = model.objects.filter(team_id=team.id)
    return_list = []
    total = 0

    for each in object_list:
        if each.__getattribute__(dependant_arg):
            return_list.append(each)
            total += each.__getattribute__(field)

    if len(return_list) == 0:
        return "None"

    return round(1000 * total / len(return_list)) / 1000


#
# {% for team in team_list %}
#     {{ team|get_pit_info:"weight" }}
# {% endfor %}
# ------- or --------
# {% get_pit_info team "field" %}
#

