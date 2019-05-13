from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from entry.models import Team, Match


def write_teleop(request, pk):
    print("Adding teleop phase to database")
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        match = Match.objects.filter(team_number=team.number).latest('match_number')

        print(team)

        # Ship Cargo
        match.ship_cargo = make_int(request.POST.get('ShipCargo', 0))
        team.ship_cargo += match.ship_cargo
        # First Cargo
        match.first_cargo = make_int(request.POST.get('FirstRocketCargo', 0))
        team.first_cargo += match.first_cargo
        # Second Cargo
        match.second_cargo = make_int(request.POST.get('SecondRocketCargo', 0))
        team.second_cargo += match.second_cargo
        # Third Cargo
        match.third_cargo = make_int(request.POST.get('ThirdRocketCargo', 0))
        team.third_cargo += match.third_cargo

        # Ship Hatch
        match.ship_hatch = make_int(request.POST.get('ShipHatch', 0))
        team.ship_hatch += match.ship_hatch
        # First Hatch
        match.first_hatch = make_int(request.POST.get('FirstRocketHatch', 0))
        team.first_hatch += match.first_hatch
        # Second Hatch
        match.second_hatch = make_int(request.POST.get('SecondRocketHatch', 0))
        team.second_hatch += match.second_hatch
        # Third Hatch
        match.third_hatch = make_int(request.POST.get('ThirdRocketHatch', 0))
        team.third_hatch += match.third_hatch

        team.save()
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
        print(team)

        # Match Setup
        match = Match()
        match.match_number = make_int(request.POST.get('MatchNumber', 0))
        match.team_number = team.number
        match.team_name = team.name

        team.matches += 1

        if make_int(request.POST.get('StartingLevel', 0)) == 1:
            match.first_start = True
            match.second_start = False
            team.first_start += 1
        else:
            match.first_start = False
            match.second_start = True
            team.second_start += 1

        # Autonomous Team
        team.auto_cargo += make_int(request.POST.get('FirstRocketCargo', 0))
        team.auto_cargo += make_int(request.POST.get('SecondRocketCargo', 0))
        team.auto_cargo += make_int(request.POST.get('ThirdRocketCargo', 0))
        team.auto_cargo += make_int(request.POST.get('ShipCargo', 0))
        team.auto_hatch += make_int(request.POST.get('FirstHatch', 0))
        team.auto_hatch += make_int(request.POST.get('SecondHatch', 0))
        team.auto_hatch += make_int(request.POST.get('ThirdHatch', 0))
        team.auto_hatch += make_int(request.POST.get('ShipHatch', 0))

        # Autonomous Match
        match.auto_cargo += make_int(request.POST.get('FirstRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('SecondRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('ThirdRocketCargo', 0))
        match.auto_cargo += make_int(request.POST.get('ShipCargo', 0))
        match.auto_hatch += make_int(request.POST.get('FirstHatch', 0))
        match.auto_hatch += make_int(request.POST.get('SecondHatch', 0))
        match.auto_hatch += make_int(request.POST.get('ThirdHatch', 0))
        match.auto_hatch += make_int(request.POST.get('ShipHatch', 0))

        team.save()
        match.save()

        print('Success')
        return HttpResponseRedirect('/entry/' + str(pk) + '/teleop/' + str(match.match_number))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


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
