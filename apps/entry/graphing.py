from django.http import QueryDict

from apps.entry.models import Match, Team
from apps.entry.errors import *


def graph(graph_type, request):
    teams = request.POST.getlist('team_list')[0].split(",")
    req_fields = request.POST.getlist('field_list')[0].split(",")

    if teams == ['']:
        print('No Team Selection \n')
        raise NoTeamsProvided

    output = {
        "bar": bar_graph(req_fields, teams),
        "overall": overall_graph(req_fields, teams),
    }

    print(graph_type)

    return output[graph_type]


def overall_graph(req_fields, teams):
    return return_home()


def bar_graph(req_fields, teams):
    default_out = Match.objects.all()[0].__dict__
    data_out = {}

    single_items = ['team_number']
    ignored_items = ['_state', 'initial_comments', 'game_comments', 'id', 'event_id', 'team_id', 'match_number']

    for item in ignored_items:
        default_out.__delitem__(item)

    for item in default_out.copy():
        if not req_fields.__contains__(item):
            default_out.__delitem__(item)

    for field in default_out:
        default_out[field] = Match._meta.get_field(field).default

    for team in teams:
        # TODO Total the values from each field per team and package the totals into a json under each team id or number
        matches = Match.objects.filter(team_id=team)
        team_data = default_out.copy()

        for match in matches:
            for field in match.__dict__:
                if team_data.__contains__(field):
                    if not (single_items.__contains__(field) and team_data[field] == default_out[field]):
                        team_data[field] += int(match.__dict__[field])

        data_out.__setitem__(str(Team.objects.filter(id=team)[0].number), team_data)

    print(data_out)
    return data_out


def decode_ajax(request):
    return dict(QueryDict(request.body.decode()))


def return_home():
    return 'lazy'
