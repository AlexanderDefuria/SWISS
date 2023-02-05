import json
import ast
import os
from json import dumps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from apps.hours.models import *
from apps.entry.views import decode_ajax, logout


@csrf_exempt
def hours_api_post(request):
    # {
    #     "UUID": "14466e66-b880-4b24-8e9b-e4ed69b38e85"
    # }
    if request.method == 'POST':
        try:
            log = Log()
            uuid = json.loads(request.body)['UUID']
            log.gremlin = Card.objects.get(uuid=uuid).user
            log.clean_and_save()
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
        return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)


class Index(generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'hours/entry.html'


class EnterHours(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'hours/entry.html'

    def post(self, request, *args, **kwargs):
        log = Log()
        log.minutes = int(request.POST.get('minutes')) + int(request.POST.get('hours')) * 60
        log.completedDate = request.POST.get('completedDate')
        log.tasks = request.POST.get('tasks')
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
        try:
            if Mentor.objects.get(user=self.request.user):
                return Log.objects.all()
        except Exception as e:
            try:
                if Gremlin.objects.get_or_create(user=self.request.user)[0]:
                    return Log.objects.all().filter(gremlin__user=self.request.user.id)
            except Exception:
                print('Nothing found at all...')
        return None

# TODO This should eventually be deprecated.
def validate_types(request, data, reqlist):
    # TODO Add emoji validation in text fields
    reqfields = {}
    redo = {}

    try:
        path = 'reqfields.json'
        path = os.path.join(settings.BASE_DIR, path)
        with open(path) as f:
            if reqlist:
                if request.path.__contains__("register"):
                    reqfields = json.load(f)['registration']
                elif request.path.__contains__("hours"):
                    reqfields = json.load(f)['hours']
                else:
                    reqfields = json.load(f)['matchScout']
    except IOError:
        print("reqfields file not found")

    print("Data:")
    print(data)

    for field in reqfields.keys():
        # This would mean someone is editing the HTML therefore we log them out to ensure data integrity.
        # print("FIELD: " + field)

        if not data.__contains__(field):
            logout(request)
            print("logged out on: " + field) # TODO Note this is logging out need to update to work with forms now.

        try:
            alpha = True
            for each in data[field][0].split():
                alpha = (alpha and each.isalpha())

            if data[field][0] != '' and not alpha and len(data[field][0].split()) == 1:
                data[field][0] = ast.literal_eval(data[field][0])
        except ValueError:
            try:
                if data[field][0] != '':
                    data[field][0] = ast.literal_eval(data[field][0][0])
            except ValueError as e:
                print("\nVALUE ERROR:")
                print(data[field])
                print(e)

        # print("type")
        # print(type(data[field][0]))
        # print(type(reqfields[field]))
        redo[field] = False if (isinstance(data[field][0], type(reqfields[field]))) else True

    for field in request.POST:
        try:
            redo[field] = not is_ascii(request.POST.get(field))
            # print(request.POST.get(field))

        except AttributeError:
            print('issue')
    if request.path.__contains__("scout") and data['scouterName'][0] == '':
        redo['scouterName'] = True

    print("Keys: " + str(redo.keys()))
    print("Needs Correcting: " + str(redo.values()))

    return redo, data

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def validate_hours(request):
    data = decode_ajax(request)
    redo, data = validate_types(request, data, True)
    return HttpResponse(dumps(redo), content_type="application/json")
