import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from apps.entry.models import Team, Match, Pits, Schedule, Result
from apps.entry.views.views import handle_query_present_teams, get_present_teams


class Glance(LoginRequiredMixin, generic.DetailView):
    login_url = 'organization:login'
    model = Team
    template_name = 'entry/glance.html'
    context_object_name = "team"

    def head(self, *args, **kwargs):
        output = {
            "test": 1
        }
        response = HttpResponse(json.dumps(output), content_type="application/json")
        return response


class GlanceLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    model = Team
    template_name = 'entry/glancelanding.html'

    def get_queryset(self):
        return handle_query_present_teams(self)

class MatchData(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    template_name = 'entry/matchdata.html'
    model = Match
    context_object_name = "match_list"

    def get_queryset(self):
        try:
            org_settings = self.request.user.orgmember.organization.settings
        except IndexError:
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))
        return Match.objects.all().filter(event_id=org_settings.current_event).filter(
            ownership=self.request.user.orgmember.organization_id)


class PitData(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    template_name = 'entry/pitdata.html'
    model = Pits

    def get_queryset(self):
        try:
            org_settings = self.request.user.orgmember.organization.settings
        except IndexError:
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return Pits.objects.all().filter(event_id=org_settings.current_event).filter(
            ownership=self.request.user.orgmember.organization_id)


class Visualize(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    template_name = 'entry/visualization.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        teams = get_present_teams(self.request.user)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))
        return teams


class ScheduleView(LoginRequiredMixin, generic.ListView):
    login_url = 'organization:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule_list"
    model = Schedule
    show_completed = False

    def get_queryset(self):
        try:
            org_settings = self.request.user.orgmember.organization.settings
        except IndexError as e:
            print(str(e) + ": There are no team settings for this query.")
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        schedule = Schedule.objects.filter(event_id=org_settings.current_event) \
            .exclude(match_number=0) \
            .order_by("match_type") \
            .order_by("match_number")
        results = Result.objects \
            .filter(event=org_settings.current_event, ownership=org_settings.organization, completed=True) \
            .values_list('match__match_number', flat=True)

        if self.show_completed:
            return schedule, results, True

        return schedule, results, False


class ScheduleDetails(LoginRequiredMixin, generic.DetailView):
    login_url = 'organization:login'
    template_name = 'entry/schedule-details.html'
    model = Schedule
    context_object_name = "schedule"
