from django.http import QueryDict

from apps.entry.models import Match, Team
from apps.entry.errors import *


def graph(graph_type, request):
    teams = request.POST.getlist('team_list')[0].split(",")
    print('Team List')
    print(request.POST.getlist('team_list')[0])
    req_fields = request.POST.getlist('field_list')[0].split(",")

    if teams == ['']:
        print('No Team Selection \n')
        raise NoTeamsProvided

    output = {
        "bar": bar_graph(req_fields, teams, request),
        "overall": overall_graph(req_fields, teams),
    }

    return output[graph_type]


def overall_graph(req_fields, teams):
    return return_home()


def bar_graph(req_fields, teams, request):
    default_out = Match.objects.all()[0].__dict__
    data_out = {}

    single_items = ['team_number']
    ignored_items = ['_state', 'id', 'event_id', 'team_id']

    for item in ignored_items:
        try:
            default_out.__delitem__(item)
        except KeyError:
            print(item + ' - Is supposed to be an ignored item but is not found - graphing.py bar_graph()')

    # Remove all the non requested items from the default list
    for item in default_out.copy():
        if not req_fields.__contains__(item):
            default_out.__delitem__(item)

    # Get the default value for each field
    for field in default_out:
        default_out[field] = Match._meta.get_field(field).default

    for team in teams:
        # TODO Total the values from each field per team and package the totals into a json under each team id or number
        matches = Match.objects.filter(team_id=team, team_ownership=request.user.teammember.team_id)
        team_data = default_out.copy()

        # TODO Separate out dependants like in glance, meaning only contribute quality to average if defense was actually played

        for match in matches:
            for field in match.__dict__:
                if team_data.__contains__(field):
                    if not (single_items.__contains__(field) and team_data[field] == default_out[field]):
                        team_data[field] += int(match.__dict__[field])

        team_data["MatchAmount"] = len(matches)
        data_out.__setitem__(str(Team.objects.filter(id=team)[0].number), team_data)

    return data_out


def decode_ajax(request):
    return dict(QueryDict(request.body.decode()))


def return_home():
    return 'lazy'
