from django import template
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from apps.entry.models import *
from apps.entry import views
from apps import config

register = template.Library()


@user_passes_test(views.scout_lead_check, login_url='entry:login')
@login_required(login_url='entry:login')
def change_event_write(request):
    if request.method == 'POST':
        config.set_event(str(request.POST.get('event', '')))

    return HttpResponseRedirect(reverse_lazy('setup:change-event'))


class Setup(generic.ListView):
    template_name = "setup/setup.html"
    context_object_name = "event_list"
    model = Event

    def get_queryset(self):
        return Event.objects.order_by("start")


class ChangeEvent(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = "setup/change-event.html"
    context_object_name = "event_list"
    model = Event

    def get_context_data(self, **kwargs):
        return {"events" : Event.objects.exclude(name__contains="***SUSPENDED***").order_by("start")}


# TODO Import FRC through Setup app
class ImportFRC(generic.TemplateView):
    template_name = "setup/import-frc.html"


class MatchEditor(generic.TemplateView):
    template_name = "setup/match-editor.html"
    context_object_name = "match_list"
    model = Match

