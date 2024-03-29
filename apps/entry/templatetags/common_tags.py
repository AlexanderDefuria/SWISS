from datetime import timedelta
import inspect
import math

from django import template
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils import timezone


from apps.entry.views.helpers import get_present_teams
from apps.entry.models import Team, Match, Pits
from apps.organization.models import Event

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
    return num % val == 0


@register.filter
def divide(num, val):
    if val == 0:
        return -1
    return num / val


@register.filter
def define(val):
    return val


@register.simple_tag
def get_current_event(request):
    try:
        # return Event.objects.filter(FIRST_key=config.get_current_event_key())[0]
        return request.user.orgmember.organization.settings.current_event
    except IndexError:
        event = Event()
        event.name = "Temp"
        event.FIRST_key = ""
        return event
    except:
        return Event.objects.all()[0]


@register.simple_tag
def get_admin_url():
    return reverse_lazy('admin:index')


@register.simple_tag
def get_edit_url(model, model_id):
    return reverse_lazy('admin:index') + 'entry/' + str(model) + '/' + str(model_id) + '/change/'


@register.simple_tag
def get_current_event_id():
    return get_current_event.id


@register.simple_tag
def get_team_name(team_number):
    try:
        return Team.objects.all().get().name
    except IndexError as e:
        return "No Such Team"


@register.simple_tag
def get_team_colour(team_number):
    try:
        return Team.objects.all().get().colour
    except IndexError as e:
        return "No Such Team"


@register.simple_tag
def get_team_onfield(user, team_number):
    try:
        total = Match.objects.all().filter(team_id=team_number,
                                           event=user.orgmember.organization.settings.current_event)
        present = total.filter(on_field=True).count()
        total = total.count()
        if total == 0:
            return 1
        return int(present / total * 100)
    except IndexError as e:
        return "NA"


@register.simple_tag
def get_match_fields():
    print([f.name for f in Match._meta.get_fields()])
    return [f.name for f in Match._meta.get_fields()]


@register.simple_tag
def get_cookie(request, cookie_name):
    result = request.COOKIES.get(cookie_name)
    return result


@register.simple_tag
def get_user_role(request):
    return request.user.orgmember


@register.simple_tag
def get_team_uuid(request):
    return str(request.user.orgmember.organization.reg_id)[:6]


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
        timediff = session.expire_date - time - timedelta(days=13, hours=23, minutes=57, seconds=30)
        if timedelta(seconds=0) < timediff:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id'))
            count += 1

    # Query all logged in users based on id list and return the length of that queryset
    if "unique" in args:
        return len(User.objects.filter(id__in=uid_list))
    else:
        return 1 if count == 0 else count  # There is always at least someone logged in


@register.simple_tag
def get_all_present_teams(user):
    return get_present_teams(user)


@register.simple_tag
def get_all_teams():
    objects = Team.objects.all()
    objects = objects.order_by('number')
    return objects


@register.simple_tag
def get_all_events():
    return Event.objects.all().order_by('start')



@register.simple_tag
def is_lead_scout(request):
    # Check if user is the highest level position
    return request.user.orgmember.position == 'LS'


@register.simple_tag
def get_gouda(team):
    try:
        gouda_list = Match.objects.filter(team_id=team).order_by('-created_at')
        gouda = 0
        n = 0
        total_weight = 0
        for i in gouda_list.iterator():
            n += 1
            i * (1 / (math.sqrt(n)))
            total_weight += (1 / (math.sqrt(n)))
            gouda += i

        return gouda / total_weight

    except IndexError as e:
        print("INDEX ERROR GOUDA TEMPLATE TAG - " + str(e))
        return


@register.simple_tag
def get_info(user, team, field, *args):
    try:
        if type(team) is type(str()):
            try:
                team = int(team)
            except ValueError as e:
                print("Passed wrong value: " + team)
                return
        if type(team) is type(int()):
            try:
                team = Team.objects.all().get()
            except IndexError as e:
                print(e)
                return

        model = Pits
        if "match" in args:
            model = Match

        if len(model.objects.all().filter(team_id=team.id,
                                          event_id=user.orgmember.organization.settings.current_event.id,
                                          ownership=user.orgmember.organization)) == 0:
            return "No Data"

        if "dependant" in args:
            return dependant(user, team, field, model, args)
        elif "average" in args:
            return get_average(user, team, field, model)
        elif "total" in args:
            return get_total(user, team, field, model)
        elif "list" in args:
            return get_list(user, team, field, model)
        elif "possible" in args:
            return get_possible(user, team, field, model)

        return "ERROR"

    except IndexError:
        return "NA"


def get_average(user, team, field, model):
    if model.objects.first()._meta.get_field(field).get_internal_type() not in (
            'IntegerField', 'SmallIntegerField', 'BooleanField'):
        result_list = get_list(user, team, field, model)
        most_common = 'None'
        occured = 0
        for each in result_list:
            if result_list.count(each) > occured:
                occured = result_list.count(each)
                most_common = each
        return most_common

    total = get_total(user, team, field, model)
    model_instances = model.objects.filter(team_id=team.id,
                                           ownership=user.orgmember.organization,
                                           event=user.orgmember.organization.settings.current_event)

    if field == 'lock_status' or field == 'endgame_action':
        most_common = model_instances.annotate(mc=Count(field)).order_by('-mc')[0].lock_status
        total = model_instances.filter(lock_status=most_common).count()
        model_instances = model.objects.filter(team_id=team.id,
                                               ownership=user.orgmember.organization,
                                               lock_status=most_common,
                                               event=user.orgmember.organization.settings.current_event)

    # If its to do with scoring or fouls return a percent
    scale = 1000 if model == Pits else 1000
    if str(field).__contains__("lock_status") or str(field).__contains__("endgame_action"):
        scale = 10

    return round(1000 * (total / len(model_instances))) / scale


def get_total(user, team, field, model):
    total = 0
    object_list = model.objects.filter(team_id=team.id,
                                       ownership=user.orgmember.organization,
                                       event=user.orgmember.organization.settings.current_event)
    boolean = model.objects.first()._meta.get_field(field).get_internal_type() == 'BooleanField'

    for entry in object_list:
        if boolean:
            if entry.__getattribute__(field):
                total += 1
        else:
            total += entry.__getattribute__(field)

    return total


def get_list(user, team, field, model):
    object_list = model.objects.filter(team_id=team.id,
                                       ownership=user.orgmember.organization,
                                       event=user.orgmember.organization.settings.current_event)
    result_list = []
    return_list = {}

    for entry in object_list:
        result_list.append(entry.__getattribute__(field))

    if inspect.stack()[1].function == 'get_info':
        # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
        for each in result_list:
            if return_list.get(each) is None:
                return_list[each] = 1
            else:
                return_list[each] += 1

        d = return_list
        return_list = {}

        for k in sorted(d, key=d.get, reverse=(not isinstance(model, Pits))):
            # print(k, d[k])
            rename = []
            if field == 'tele_positions':
                rename = ["Against Fender", "Tarmac", "Launch Pad", "Anywhere"]
            elif field == 'field_timeout_pos':
                rename = ["Nothing", "Parked", "Attempted Climb", "Successful Climb"]
            elif field == 'lock_status':
                rename = ["No Attempt", "Low Rung", "Mid Rung", "High Rung", "Traversal"]
            elif field == 'endgame_action':
                rename = ["No Attempt", "Low Rung", "Mid Rung", "High Rung", "Traversal"]

            if rename is not []:
                # print("\nd[" + str(k) + "]: " + str(d[k]))
                # print("rename[" + str(k) + "]: " + str(rename[k]))
                # print("return_list: " + str(d[k]))
                return_list[rename[k]] = d[k]
            else:
                return_list[k] = d[k]

        return list(return_list)

    else:
        return result_list


def get_possible(user, team, field, model):
    object_list = model.objects.filter(team_id=team.id,
                                       ownership=user.orgmember.organization,
                                       event=user.orgmember.organization.settings.current_event)
    default = model._meta.get_field(field).default

    # print("DEFAULT: " + str(default))
    for each in object_list:
        if each.__getattribute__(field) != default:
            return "Yes"

    return "No"


def dependant(user, team, field, model, args):
    dependant_arg = ''
    for arg in args:
        if "dependant-" in str(arg):
            dependant_arg = str(arg)[10:]
            continue
        if args.index(arg) == len(args) - 1:
            return 0

    object_list = model.objects.filter(team_id=team.id,
                                       ownership=user.orgmember.organization,
                                       event=user.orgmember.organization.settings.current_event)
    return_list = []
    total = 0

    for each in object_list:
        if each.__getattribute__(dependant_arg):
            return_list.append(each)
            total += each.__getattribute__(field)

    if len(return_list) == 0:
        return "None"

    return round(1000 * total / len(return_list)) / 1000
