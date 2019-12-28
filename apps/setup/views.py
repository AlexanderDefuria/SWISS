from django.views import generic
from ..entry.models import Team, Event


class Setup(generic.ListView):
    template_name = "setup/setup.html"
    context_object_name = "event_list"
    model = Event

    def get_queryset(self):
        return Event.objects.order_by("start")


class ImportTBA(generic.TemplateView):
    template_name = "setup/import-tba.html"


class Teams(generic.DetailView):
    template_name = "setup/detail-view.html"


