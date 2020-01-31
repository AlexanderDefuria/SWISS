import base64
import os
from json import dumps

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from apps import config
from apps.entry.graphing import *
from apps.entry.models import Team, Match, Schedule


def write_teleop(request, pk):
    print("Adding teleop phase to database")
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        match = Match.objects.filter(team_id=team.id).latest('match_number')

        print(team)
        print(request.POST)

        match.ship_cargo = make_int(request.POST.get('ship_cargo', 0))
        match.first_cargo = make_int(request.POST.get('first_cargo', 0))
        match.second_cargo = make_int(request.POST.get('second_cargo', 0))
        match.third_cargo = make_int(request.POST.get('third_cargo', 0))

        match.ship_hatch = make_int(request.POST.get('ship_hatch', 0))

        match.first_hatch = make_int(request.POST.get('first_hatch', 0))
        match.second_hatch = make_int(request.POST.get('second_hatch', 0))
        match.third_hatch = make_int(request.POST.get('third_hatch', 0))

        match.defense_time = make_int(request.POST.get('defense_time', 0))

        match.climb = make_int(request.POST.get('climb_level', 0))

        match.comments = request.POST.get('comments', 0)

        match.save()

        print('Success')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


def write_auto(request, pk):
    print("Adding auto phase to database")
    if request.method == 'POST':
        team = Team.objects.get(id=pk)

        # Match Setup
        match = Match()
        match.match_number = make_int(request.POST.get('MatchNumber', 0))
        match.event_id = config.current_event_id
        if match.event_id != config.current_event_id:
            raise Http404
        match.team_id = team.id

        match.start = make_int(request.POST.get('starting_level'))

        # Autonomous Match
        match.auto_cargo += make_int(request.POST.get('first_cargo', 0))
        match.auto_cargo += make_int(request.POST.get('second_cargo', 0))
        match.auto_cargo += make_int(request.POST.get('third_cargo', 0))
        match.auto_cargo += make_int(request.POST.get('ship_cargo', 0))
        match.auto_hatch += make_int(request.POST.get('first_hatch', 0))
        match.auto_hatch += make_int(request.POST.get('second_hatch', 0))
        match.auto_hatch += make_int(request.POST.get('third_hatch', 0))
        match.auto_hatch += make_int(request.POST.get('ship_hatch', 0))

        match.save()

        print('Success')
        return HttpResponseRedirect('/entry/' + str(pk) + '/teleop/' + str(match.match_number))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


def view_matches(request):
    if request.method == 'GET':
        print("POSTED")
    return HttpResponseRedirect(reverse_lazy('entry:view_matches'))


@ajax
@csrf_exempt
def update_graph(request):
    data = decode_ajax(request)
    create_teams_graph(data)

    try:
        image_data = base64.b64encode(open( str(settings.BASE_DIR) + "/media/dynamic_plot.png", "rb").read())
        return HttpResponse(image_data, content_type="image/png")
    except IOError:
        print("Image not found")
        return Http404


@ajax
@csrf_exempt
def validate_match(request, pk):
    # The parsing of the db to check if a team has played at a particular match already is done server side
    # The ajax post sends only the match number in a JSON file to comply with AJAX datatype specification
    # dumps() is to convert dictionary into JSON format for HttpResponse to keep it simple stupid

    data = decode_ajax(request)['match_number']
    provided_match_number = make_int(data[0])
    result = {'result': False}

    if not Match.objects.filter(team_id=pk, event_id=config.current_event_id,
                                match_number=provided_match_number).exists():
        if Match.objects.filter(match_number=provided_match_number).count() < 6:
            result['result'] = True

    return HttpResponse(dumps(result), content_type="application/json")


def decode_ajax(request):
    return dict(QueryDict(request.body.decode()))


def download(request):
    path = './db.sqlite3'

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def make_int(s):
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams():
    x = Team.objects.filter(event_one_id=config.current_event_id)
    x = x | Team.objects.filter(event_two_id=config.current_event_id)
    x = x | Team.objects.filter(event_three_id=config.current_event_id)
    x = x | Team.objects.filter(event_four_id=config.current_event_id)
    return x.order_by('number')


class TeamNumberList(generic.ListView):
    template_name = 'entry/landing.html'
    context_object_name = "team_list"
    model = Team

    def get_queryset(self):
        return get_present_teams()


class Auto(generic.DetailView):
    model = Team
    template_name = 'entry/auto.html'


class Teleop(generic.DetailView):
    model = Team
    template_name = 'entry/teleop.html'


class EventSetup(generic.TemplateView):
    template_name = 'entry/event-setup.html'


class Visualize(generic.TemplateView):
    template_name = 'entry/visualize.html'


class ScheduleView(generic.ListView):
    template_name = 'entry/schedule.html'
    context_object_name = "schedule"
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(event_id=config.current_event_id).order_by("match_type")
