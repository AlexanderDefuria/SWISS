import os

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy
from django.views import generic
from entry.models import Team, Match
from entry import config


def write_teleop(request, pk):
    print("Adding teleop phase to database")
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        match = Match.objects.filter(team_id=team.id).latest('match_number')

        print(team)

        # Ship Cargo
        match.ship_cargo = make_int(request.POST.get('ShipCargo', 0))
        # First Cargo
        match.first_cargo = make_int(request.POST.get('FirstRocketCargo', 0))
        # Second Cargo
        match.second_cargo = make_int(request.POST.get('SecondRocketCargo', 0))
        # Third Cargo
        match.third_cargo = make_int(request.POST.get('ThirdRocketCargo', 0))

        # Ship Hatch
        match.ship_hatch = make_int(request.POST.get('ShipHatch', 0))
        # First Hatch
        match.first_hatch = make_int(request.POST.get('FirstRocketHatch', 0))
        # Second Hatch
        match.second_hatch = make_int(request.POST.get('SecondRocketHatch', 0))
        # Third Hatch
        match.third_hatch = make_int(request.POST.get('ThirdRocketHatch', 0))

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
        match.event_id = config.get_event(config.current_event)
        if match.event_id != team.cur_event:
            raise Http404
        match.team_id = team.id

        if make_int(request.POST.get('StartingLevel', 0)) == 1:
            match.first_start = True
            match.second_start = False
        else:
            match.first_start = False
            match.second_start = True

        # Autonomous Match
        match.auto_cargo += make_int(request.POST.get('FirstRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('SecondRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('ThirdRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('ShipCargo', 0))
        match.auto_hatch += make_int(request.POST.get('FirstHatch', 0))
        match.auto_hatch += make_int(request.POST.get('SecondHatch', 0))
        match.auto_hatch += make_int(request.POST.get('ThirdHatch', 0))
        match.auto_hatch += make_int(request.POST.get('ShipHatch', 0))

        match.save()

        print('Success')
        return HttpResponseRedirect('/entry/' + str(pk) + '/teleop/' + str(match.match_number))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


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


class TeamNumberList(generic.ListView):
    template_name = 'entry/landing.html'
    context_object_name = "team_list"

    def get_queryset(self):
        return Team.objects.order_by('name')


class Auto(generic.DetailView):
    model = Team
    template_name = 'entry/auto.html'


class Teleop(generic.DetailView):
    model = Team
    template_name = 'entry/teleop.html'


class EventSetup(generic.TemplateView):
    template_name = 'entry/event-setup.html'
