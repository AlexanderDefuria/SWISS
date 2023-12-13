import json
import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.postgres import serializers
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from swiss import settings
from apps.entry.errors import NoTeamsProvided, NoFieldsProvided
from apps.entry.graphing import graph
from apps.entry.models import Match, Team
from apps.entry.views.views import make_int, update_csv


@ajax
@csrf_exempt
@login_required(login_url='organization:login')
def update_fields(request):
    if request.method == "GET":
        try:
            path = 'scoring.json'
            path = os.path.join(settings.BASE_DIR, path)
            with open(path) as f:
                result = json.load(f)
            return JsonResponse(result)
        except IOError:
            print("Fields file not found")
            return Http404
    else:
        return HttpResponseRedirect(reverse_lazy('entry:visualize'))


@ajax
@csrf_exempt
@login_required(login_url='organization:login')
def update_graph(request):
    graph_type = request.POST.getlist('graphType')[0]
    try:
        output = graph(graph_type, request)
        if output == "lazy":
            return HttpResponseRedirect(reverse_lazy('entry:visualize'))
        print(output)
        response = HttpResponse(json.dumps(output), content_type="application/json")
        return response
    except IOError:
        print("Image not found")
        return Http404
    except NoTeamsProvided:
        return NoTeamsProvided
    except NoFieldsProvided:
        return NoFieldsProvided


@ajax
@csrf_exempt
@login_required(login_url='organization:login')
def update_glance(request, pk):
    matches = Match.objects.filter(team_id=pk,
                                   ownership_id=request.user.orgmember.organization_id).order_by('event',
                                                                                                 'match_number')
    count = matches.count()
    try:
        if make_int(Team.objects.get(id=pk).glance.name.split('_')[2]) == count:
            return HttpResponse(Team.objects.get(id=pk).glance.read(), content_type='application/json')
    except IndexError:
        print("")
    except AttributeError:
        print("")
    except FileNotFoundError:
        print("Creating new glance json file for " + str(Team.objects.get(id=pk).glance))

    matches_json = serializers.serialize('json', matches)
    if not settings.USE_MEDIA_SPACES:
        f = open(os.path.join(settings.BASE_DIR, 'glance_temp.json'), 'w')
        f.write(str(matches_json))
        f = open(os.path.join(settings.BASE_DIR, 'glance_temp.json'), 'r', encoding='UTF-8')
        team = Team.objects.get(id=pk)
        team.glance.delete()
        team.glance.save(
            'glance_' + str(pk) + '_' + str(count) + '_' + str(datetime.now()) + '.json', f)
    return HttpResponse(matches_json, content_type='application/json')


@ajax
@csrf_exempt
@login_required(login_url='organization:login')
def get_csv_ajax(request):
    path = 'match_history.xlsx'
    path = os.path.join(settings.BASE_DIR, path)
    update_csv(request.user.orgmember.organization)

    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/xlsx")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response
    return Http404

