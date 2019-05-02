from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from entry.models import Team


def write_cargo(request, pk):
    print("adding to database")
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        print(team)

        # First Cargo
        team.first_cargo = team.first_cargo + make_int(request.POST.get('FirstRocketCargo', 0))
        # Second Cargo
        team.second_cargo = team.second_cargo + make_int(request.POST.get('SecondRocketCargo', 0))
        # Third Cargo
        team.third_cargo = team.third_cargo + make_int(request.POST.get('ThirdRocketCargo', 0))

        # First Cargo
        team.first_hatch = team.first_hatch + make_int(request.POST.get('FirstRocketHatch', 0))
        # Second Hatch
        team.second_hatch = team.second_hatch + make_int(request.POST.get('SecondRocketHatch', 0))
        # Third Hatch
        team.third_hatch = team.third_hatch + make_int(request.POST.get('ThirdRocketHatch', 0))

        team.save()

        print('Success')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))

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
