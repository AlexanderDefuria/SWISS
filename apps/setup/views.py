from django import template
from django.http import HttpResponseRedirect
from django.template.defaultfilters import stringfilter
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from apps.entry.models import Team, Event
from apps import config

register = template.Library()


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

    @register.filter
    def modulo(self, num, val):
        return num % val == 0


class ChangeEvent(generic.TemplateView):
    template_name = "setup/change-event.html"
    context_object_name = "event_list"
    model = Event

    def get_context_data(self, **kwargs):
        return {"events" : Event.objects.exclude(name__contains="***SUSPENDED***").order_by("start")}


class ImportTBA(generic.TemplateView):
    template_name = "setup/import-tba.html"


class Teams(generic.DetailView):
    template_name = "setup/detail-view.html"


