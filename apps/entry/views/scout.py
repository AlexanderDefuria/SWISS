from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.entry.forms import MatchScoutForm, PitScoutForm
from apps.entry.models import Team, Match, Pits
from apps.entry.views.views import make_int, get_present_teams
from apps.organization.models import Event


class MatchScout(LoginRequiredMixin, FormMixin, generic.DetailView):
    login_url = 'organization:login'
    model = Team
    template_name = 'entry/matchscout.html'
    form_class = MatchScoutForm
    success_url = 'entry:match_scout_landing'

    @staticmethod
    def post(request, pk, *args, **kwargs):
        org_settings = request.user.orgmember.organization.settings

        form = MatchScoutForm(request.POST,
                              event=org_settings.current_event,
                              ownership=request.user.orgmember.organization)
        team = Team.objects.get(id=pk)
        context = {'form': form, 'team': team}

        if form.is_valid():
            print("Valid Match Scout")
            print(form.cleaned_data)
            first_key = Event.objects.all().filter(id=make_int(org_settings.current_event.id))[0].FIRST_key

            auto_start_x, auto_start_y = form.cleaned_data.pop('auto_start')
            match = Match(**form.cleaned_data)
            match.auto_start_x = auto_start_x
            match.auto_start_y = auto_start_y
            match.team = team
            match.event = Event.objects.get(FIRST_key=first_key)
            match.scouter_name = request.user.username
            match.ownership = request.user.orgmember.organization
            try:
                match.save()
                print('Match Scout Submission Success')
            except Exception as e:
                print(e)

            print(match)

            return HttpResponseRedirect(reverse_lazy('entry:match_scout_landing'))

        return render(request, 'entry/matchscout.html', context)


class MatchScoutLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    model = Team
    context_object_name = "team_list"
    template_name = 'entry/matchlanding.html'

    def get_queryset(self):
        return get_present_teams(self.request.user)


class PitScout(LoginRequiredMixin, FormMixin, generic.DetailView):
    login_url = 'organization:login'
    template_name = 'entry/pitscout.html'
    model = Team
    context_object_name = "team"
    form_class = PitScoutForm
    success_url = 'entry:pit_scout_landing'

    @staticmethod
    def post(request, pk, *args, **kwargs):
        form = PitScoutForm(request.POST)
        team = Team.objects.get(id=pk)
        context = {'form': form, 'team': team}

        if form.is_valid():
            pits = Pits(**form.cleaned_data)
            # TODO Finish This
            return HttpResponseRedirect(reverse_lazy('entry:pit_scout_landing'))
        return render(request, 'entry/pitscout.html', context)


class PitScoutLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    template_name = 'entry/pitlanding.html'
    context_object_name = "team_list"

    def get_queryset(self):
        teams = get_present_teams(self.request.user)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return teams

