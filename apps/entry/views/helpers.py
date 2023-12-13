from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from apps.entry.models import Team, Attendance
from apps.organization.models import OrgSettings


def make_int(s):
    if isinstance(s, str):
        if len(s) == 0:
            return 0
    if s == 'False':
        return False
    elif s == 'True':
        return True
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams(user):
    try:
        # TODO See if this is actually the best way to query all teams from attendance...
        # Note. We do need the actual Team objects (name, number, colour etc...) all that jazz
        objects = Team.objects.filter(
            number__in=Attendance.objects.filter(
                event=user.orgmember.organization.settings.current_event
            ).values_list('team_id', flat=True)
        )
        return objects
    except OrgSettings.DoesNotExist:
        return Team.objects.all()


def handle_query_present_teams(view):
    teams = get_present_teams(view.request.user)
    if teams.count() == 1 and teams.first() == Team.objects.first():
        return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

    return teams