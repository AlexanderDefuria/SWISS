import base64
import csv
import json
import os
import sqlite3
import ast

from django.core import serializers
from django.shortcuts import render_to_response

from apps import config
import dbTools

from datetime import datetime
from json import dumps

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict, JsonResponse, FileResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template import Library, loader, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test

from apps.entry.graphing import *
from apps.entry.models import Team, Match, Schedule, Images, Event, Pits

register = Library


@login_required(login_url='entry:login')
def match_scout_submit(request, pk):
    if request.method == 'POST':

        print(request.POST)



        # TODO 1. add auto route

        team = Team.objects.get(id=pk)
        match = Match()
        match.team = team
        match.event = Event.objects.get(FIRST_key=config.get_current_event_key())

        match_number = request.POST.get('matchNumber', -1)
        match.match_number = match_number if match_number is not '' else -1

        match.on_field = request.POST.get('onField', False)
        match.auto_start = request.POST.get('autoStart', 10)
        match.preloaded_balls = request.POST.get('preloadedBalls', 3)

        match.auto_route = request.POST.get('autoRoute', 0)
        match.baseline = request.POST.get('baseline', False)
        match.outer_auto = request.POST.get('outerAuto', 0)
        match.lower_auto = request.POST.get('lowerAuto', 0)
        match.inner_auto = request.POST.get('innerAuto', 0)
        match.auto_comment = request.POST.get('autoComment', '')

        match.outer = request.POST.get('outer', 0)
        match.lower = request.POST.get('lower', 0)
        match.inner = request.POST.get('inner', 0)
        match.wheel_score = request.POST.get('wheelScore', 0)
        match.wheel_rating = request.POST.get('wheelRating', 0)
        match.fouls = request.POST.get('offensiveFouls', 0)
        match.missed_balls = request.POST.get('missedBalls', 0)
        match.ball_intake_type = request.POST.get('intakeType', 0)
        match.under_defense = request.POST.get('underDefense', 0)
        match.cycle_style = int(request.POST.get('cycleStyle', 0))

        match.defense_rating = request.POST.get('defenseRating', 0)
        match.defense_fouls = request.POST.get('defenseFouls', 0)
        team_defended = request.POST.get('teamDefended', '')
        match.team_defended = team_defended if team_defended is not '' else -1
        # TODO Fix able to push, there is an incorrect associated input type
        match.able_to_push = 0

        if request.POST.get('climb_location', 0) == 0:
            match.climb = False
        else:
            match.climb = True
        match.climb_location = request.POST.get('climb_location', 0)
        match.field_timeout_pos = request.POST.get('lockStatus', 0)

        match.hp_fouls = request.POST.get('fouls_hp', 0)
        match.dt_fouls = request.POST.get('fouls_driver', 0)
        match.yellow_card = True if request.POST.get('yellow_card', 0) is not '' else False

        match.scouter_name = request.POST.get('scouter_name', '')

        match.save()

        print(match)

        print('Success')
        return HttpResponseRedirect(reverse_lazy('entry:match_scout_landing'))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:match_scout_landing'))


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def validate_match_scout(request, pk):
    # The parsing of the db to check if a team has played at a particular match already is done server side
    # The ajax post sends only the match number in a JSON file to comply with AJAX datatype specification
    # dumps() is to convert dictionary into JSON format for HttpResponse to keep it simple stupid

    data = decode_ajax(request)

    redo, data = validate_types(request, data)

    if data['matchNumber'][0] == 0:
        redo['matchNumber'] = True


    if Match.objects.filter(team_id=pk, event_id=config.get_current_event_id(),
                               match_number=data['matchNumber'][0]).exists():
        # Check if there are already 6 teams that have played this match
        if Match.objects.filter(match_number=data['matchNumber'][0]).count() <= 6:
            redo['matchNumber'] = True

    return HttpResponse(dumps(redo), content_type="application/json")


@login_required(login_url='entry:login')
def validate_types(request, data):
    reqfields = {}
    redo = {}

    try:
        path = 'reqfields.json'
        path = os.path.join(settings.BASE_DIR, path)
        with open(path) as f:
            reqfields = json.load(f)['matchScout']
    except IOError:
        print("reqfields file not found")

    print(data)

    for field in reqfields.keys():
        # This would mean someone is editing the HTML therefore we log them out to ensure data integrity.

        print("FIELD " + field)

        if not data.__contains__(field):
            logout(request)

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

        redo[field] = False if (isinstance(data[field][0], type(reqfields[field]))) else True

    if data['scouterName'][0] == '':
        redo['scouterName'] = True

    return redo, data


@login_required(login_url='entry:login')
def pit_scout_submit(request, pk):
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        pits = Pits()

        pits.team = team
        pits.event = Event.objects.get(FIRST_key=config.get_current_event_key())

        pits.drivetrain_style = request.POST.get('drivetrain_style', ' ')
        pits.drivetrain_wheels = request.POST.get('drivetrain_wheels', ' ')
        pits.drivetrain_motortype = request.POST.get('drivetrain_motortype', ' ')
        pits.drivetrain_motorquantity = request.POST.get('drivetrain_motorquantity', 0)

        pits.auto_route = request.POST.get('auto_route', False)
        pits.auto_description = request.POST.get('auto_description', ' ')
        pits.auto_scoring = request.POST.get('auto_scoring', 0)

        pits.tele_scoring = request.POST.get('tele_scoring', 0)
        pits.tele_positions = request.POST.get('tele_positions', 0)

        pits.ball_intake = request.POST.get('ball_intake', ' ')
        pits.ball_capacity = request.POST.get('ball_capacity', 0)
        pits.shooter_style = request.POST.get('shooter_style', ' ')
        pits.low_bot = request.POST.get('low_bot', False)
        pits.wheel_manipulator = request.POST.get('wheel_manipulator', False)
        pits.weight = request.POST.get('weight', 0)

        pits.climb_locations = request.POST.get('climb_locations', 0)
        pits.climb_buddy = request.POST.get('climb_buddy', False)
        pits.climb_balance = request.POST.get('climb_balance', False)

        pits.scouter_name = request.POST.get('scouter_name', '0')

        pits.save()

        print(pits)

        print('Success')
        return HttpResponseRedirect(reverse_lazy('entry:pit_scout_landing'))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:pit_scout_landing'))


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def validate_pit_scout(request, pk):
    return HttpResponseRedirect(reverse_lazy('entry:index'))


def view_matches(request):
    if request.method == 'GET':
        print("POSTED")
    return HttpResponseRedirect(reverse_lazy('entry:visualize'))


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def update_graph(request):
    graph_type = request.POST.getlist('graphType')[0]

    try:
        output = graph(graph_type, request)
        if output == "lazy":
            return HttpResponseRedirect(reverse_lazy('entry:visualize'))
        print(output)
        response = HttpResponse(dumps(output), content_type="application/json")
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
@login_required(login_url='entry:login')
def update_glance(request, pk):
    matches = Match.objects.filter(team_id=pk)
    matches_json = serializers.serialize('json', matches)
    return HttpResponse(matches_json, content_type='application/json')


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def update_fields(request):
    data = decode_ajax(request)

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


def decode_ajax(request):
    return dict(QueryDict(request.body.decode()))


def scout_lead_check(user):
    return user.groups.filter(name="Scouting").exists()


# TODO Export into .xls instead of .csv
# @user_passes_test(scout_lead_check, login_url='entry:login')
@login_required(login_url='entry:login')
def download(request):
    path = 'match_history.csv'
    path = os.path.join(settings.BASE_DIR, path)
    update_csv()

    if request.method == "GET" and os.path.exists(path):

        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response

    return Http404


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def get_csv_ajax(request):
    path = 'match_history.csv'
    path = os.path.join(settings.BASE_DIR, path)
    update_csv()

    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response
    return Http404


def update_csv():
    print("Updating CSV File")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM entry_match WHERE event_id=?", (config.get_current_event_id(),))
    with open("match_history.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in c.description])
        csv_writer.writerows(c)


@login_required(login_url='entry:login')
def write_image_upload(request):
    if request.method == 'POST':
        team_number = make_int(request.POST.get('teamNumber', 0))
        team = Team.objects.get(number=team_number)

        request.session.set_test_cookie()

        files = request.FILES
        files = files.popitem()[1]

        for file in files:
            file.name = str(team_number) + "-----" + str(datetime.now()).replace('.', '') + '.jpg'
            image = Images(name=team.name, image=file)
            image.save()
            team.images.add(image)
            team.save()
        return HttpResponseRedirect(reverse_lazy('entry:index'))
    else:
        return HttpResponseRedirect(reverse_lazy('entry:index'))


@login_required(login_url='entry:login')
def write_pit_upload(request):
    if request.method == 'POST':
        team_number = 0
    else:
        return HttpResponseRedirect(reverse_lazy('entry:index'))


def login(request):
    print(request.method)
    if request.method == 'GET':
        template = loader.get_template('entry/login.html')

        if request.user.is_authenticated:
            logout(request)

        return HttpResponse(template.render({}, request))

    elif request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print(auth)

        return HttpResponseRedirect(reverse_lazy('entry:index'))

    return HttpResponseRedirect(reverse_lazy('entry:login'))


@login_required(login_url='entry:login')
def logout(request):
    auth.logout(request)
    print("request.user.is_authenticated:" + str(request.user.is_authenticated))
    return HttpResponseRedirect(reverse_lazy('entry:index'))


def handler404(request, exception, template_name="entry/secret.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def make_int(s):
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams():
    event_key = config.get_current_event_key()
    objects = Team.objects.filter(number__in=dbTools.get_event_teams(event_key))
    objects = objects.order_by('number')
    return objects


class TeamList(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/teams.html'
    context_object_name = "team_list"
    model = Team

    def get_queryset(self):
        return get_present_teams()


class Index(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/index.html'
    model = Team


class MatchScout(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/matchscout.html'


class MatchScoutLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    model = Team
    context_object_name = "team_list"
    template_name = 'entry/matchlanding.html'

    def get_queryset(self):
        return get_present_teams()


class Visualize(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/visualization.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        return get_present_teams()


# class ImageUpload(LoginRequiredMixin, generic.TemplateView):
#     login_url = 'entry:login'
#     template_name = 'entry/image-upload.html'
#     model = Team
#     context_object_name = "team_list"


# DPERECATED
class ImageViewer(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/image-viewer.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        return get_present_teams()


# DPERECATED
class ScheduleView(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule"
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(event_id=config.current_event_id).order_by("match_type")


class PitScout(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    template_name = 'entry/pitscout.html'
    model = Team

    context_object_name = "team"


class PitScoutLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/pitlanding.html'
    context_object_name = "team_list"

    def get_queryset(self):
        return get_present_teams()


class Experimental(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/experimental.html'


class About(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/about.html'


class Glance(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/glance.html'
    context_object_name = "team"


class GlanceLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/glance.html'


class Data(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/data.html'


class Upload(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/upload.html'
