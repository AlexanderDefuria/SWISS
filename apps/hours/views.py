from json import dumps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from apps.hours.models import *
from apps.entry.views import decode_ajax, validate_types


class EnterHours(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'hours/entry.html'

    def post(self, request, *args, **kwargs):
        try:
            if Log.objects.all().get(completedDate=request.POST.get('completedDate', ' ')):
                return HttpResponse(status=204)
        except Exception as e:
            print(e)

        log = Log()
        log.minutes = int(request.POST.get('minutes', 0)) + int(request.POST.get('hours', 0)) * 60
        log.completedDate = request.POST.get('completedDate', ' ')
        log.tasks = request.POST.get('tasks', ' ')
        if int(log.minutes) <= 0:
            return HttpResponse(status=204)

        log.gremlin = Gremlin.objects.get_or_create(user=request.user)[0]
        log.save()
        return HttpResponseRedirect(reverse_lazy('hours:view'))


class ViewHours(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'hours/view.html'
    model = Log
    context_object_name = 'log_list'

    def post(self, request, *args, **kwargs):
        output = {"error": "noError"}
        try:
            Log.objects.get(request.POST.get('user')).status = request.POST.get('id')
        except Exception as e:
            output["error"] = str(e)
        response = HttpResponse(dumps(output), content_type="application/json")
        return response

    def get_queryset(self):
        if Mentor.objects.get(user=self.request.user):
            return Log.objects.all()
        elif Gremlin.objects.get(user=self.request.user):
            return Log.objects.all().filter(gremlin__user=self.request.user.id)


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def validate_hours(request):
    data = decode_ajax(request)
    redo, data = validate_types(request, data, True)
    return HttpResponse(dumps(redo), content_type="application/json")
