from json import dumps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from apps.hours.models import *


class EnterHours(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'hours/entry.html'

    def post(self, request, *args, **kwargs):
        log = Log()
        log.minutes = request.POST.get('minutes', 0) + request.POST.get('hours', 0) * 60
        if log.minutes <= 0:
            return HttpResponse(status=428)
        log.gremlin = Gremlin.objects.get_or_create(request.user)[0]
        log.save()
        return HttpResponse(status=204)


class ViewHours(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'hours/view.html'
    model = Log

    def post(self, request, *args, **kwargs):
        output = {"error": "noError"}
        try:
            Log.objects.get(request.POST.get('user')).status = request.POST.get('id')
        except Exception as e:
            output["error"] = str(e)
        response = HttpResponse(dumps(output), content_type="application/json")
        return response

    def get_queryset(self):
        if self.request.user is Mentor:
            return Log.objects.all()
        elif self.request.user is Gremlin:
            return Log.objects.get(gremlin__user=self.request.user)
