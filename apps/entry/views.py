import base64
import csv
import json
import os
import sqlite3
import ast

from django.core import serializers
from django.shortcuts import render_to_response

from apps import config
from apps import importFRC
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
from apps.entry.models import *
from apps.entry.templatetags import common_tags

register = Library


@login_required(login_url='entry:login')
def match_scout_submit(request, pk):
    if request.method == 'POST':

        print(request.POST)

        team = Team.objects.get(id=pk)
        match = Match()
        match.team = team
        match.event = Event.objects.get(FIRST_key=config.get_current_event_key())
        match_number = request.POST.get('matchNumber', -1)
        match.match_number = match_number if match_number != '' else -1
        match.on_field = request.POST.get('onField', False)
        match.auto_start = request.POST.get('autoStart', 10)
        match.preloaded_balls = request.POST.get('preloadedBalls', 3)
        match.auto_route = request.POST.get('autoRoute', 0)
        match.baseline = request.POST.get('baseline', False)
        match.outer_auto = request.POST.get('outer_auto', 0)
        match.lower_auto = request.POST.get('lower_auto', 0)
        match.inner_auto = request.POST.get('inner_auto', 0)
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
        if type(request.POST.get('defendedBy', 0)) is not type(int()):
            match.defended_by = 0
        else:
            match.defended_by = request.POST.get('defendedBy', 0)
        match.played_defense = request.POST.get('playedDefense', False)
        match.defense_rating = request.POST.get('defenseRating', 0)
        match.defense_fouls = request.POST.get('defenseFouls', 0)
        match.able_to_push = request.POST.get('pushRating', 0)

        team_defended = request.POST.get('teamDefended', '')
        match.team_defended = team_defended if team_defended != '' else -1

        match.climb_location = request.POST.get('climbLocation', 0)
        match.field_timeout_pos = request.POST.get('lockStatus', 0)

        match.climbed = 1 if match.field_timeout_pos == 3 else 0

        match.hp_fouls = request.POST.get('humanFouls', 0)
        match.dt_fouls = request.POST.get('driverFouls', 0)
        match.yellow_card = True if request.POST.get('cardFouls', 0) != '' else False
        match.yellow_card_descrip = request.POST.get('cardFouls', '') if match.yellow_card else 'No Foul'

        match.scouter_name = request.POST.get('scouterName', '')
        match.comment = request.POST.get('comment', '')
        match.team_ownership = request.user.teammember.team

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

    redo, data = validate_types(request, data, True)

    if data['matchNumber'][0] == 0:
        redo['matchNumber'] = True

    if Match.objects.filter(team_id=pk, event_id=config.get_current_event_id(),
                            match_number=data['matchNumber'][0]).exists():
        # Check if there are already 6 teams that have played this match
        if Match.objects.filter(match_number=data['matchNumber'][0]).count() <= 6:
            redo['matchNumber'] = True

    return HttpResponse(dumps(redo), content_type="application/json")


@login_required(login_url='entry:login')
def validate_types(request, data, reqlist):
    # TODO Add emoji validation in text fields

    reqfields = {}
    redo = {}

    try:
        path = 'reqfields.json'
        path = os.path.join(settings.BASE_DIR, path)
        with open(path) as f:
            if reqlist:
                reqfields = json.load(f)['matchScout']
    except IOError:
        print("reqfields file not found")

    print(data)

    for field in reqfields.keys():
        # This would mean someone is editing the HTML therefore we log them out to ensure data integrity.

        print("FIELD " + field)

        if not data.__contains__(field):
            logout(request)
            print("logged out on: " + field)

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

    for field in request.POST:
        try:
            redo[field] = not is_ascii(request.POST.get(field))
            print(request.POST.get(field))

        except AttributeError:
            print('issue')
    if data['scouterName'][0] == '':
        redo['scouterName'] = True

    print(redo.keys())
    print(redo.values())
    #    redo.__delitem__('Cleanup')

    return redo, data


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


@login_required(login_url='entry:login')
def pit_scout_submit(request, pk):
    if request.method == 'POST':

        print(request.POST)

        team = Team.objects.get(id=pk)
        pits = Pits()

        pits.team = team
        pits.event = Event.objects.get(FIRST_key=config.get_current_event_key())
        pits.drivetrain_style = request.POST.get('drivetrainStyle', ' ')
        pits.drivetrain_wheels = request.POST.get('drivetrainWheels', ' ')
        pits.drivetrain_motortype = request.POST.get('drivetrainMotor', ' ')
        pits.drivetrain_motorquantity = request.POST.get('drivetrainMotorAmount', 0)
        pits.auto_route = request.POST.get('hasAuto', False)
        pits.auto_description = request.POST.get('autoDescription', ' ')
        pits.auto_scoring = request.POST.get('autoScoring', 0)
        pits.tele_scoring = request.POST.get('teleScoring', 0)
        pits.tele_positions = request.POST.get('telePositions', 0)
        pits.ball_intake = request.POST.get('ballIntake', ' ')
        pits.ball_capacity = request.POST.get('ballCapacity', 0)
        pits.shooter_style = request.POST.get('shooterStyle', ' ')
        pits.low_bot = request.POST.get('lowBot', False)
        pits.wheel_manipulator = request.POST.get('wheelManipulator', False)
        pits.weight = request.POST.get('weight', 0)
        pits.climb_locations = request.POST.get('climbLocations', 0)
        pits.climb_buddy = request.POST.get('climbBuddy', False)
        pits.climb_balance = request.POST.get('climbBalance', False)
        pits.scouter_name = request.POST.get('scouterName', '0')
        pits.team_ownership = request.user.teammember.team
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
    data = decode_ajax(request)
    redo, data = validate_types(request, data, False)
    return HttpResponse(dumps(redo), content_type="application/json")


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
    print(request.POST)
    matches = Match.objects.filter(team_id=pk, team_ownership_id=request.user.teammember.team_id).order_by(
        'match_number')
    matches_json = serializers.serialize('json', matches)
    print(matches_json)

    return HttpResponse(matches_json, content_type='application/json')


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
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
            if not TeamMember.objects.filter(user=user).exists():
                TeamMember.objects.create(user_id=user.id)

        return HttpResponseRedirect(reverse_lazy('entry:index'))

    return HttpResponseRedirect(reverse_lazy('entry:login'))


@login_required(login_url='entry:login')
def import_from_first(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse_lazy('entry:import'))

    elif request.method == 'POST':
        import_type = make_int(request.POST.get('importType', 0))
        key = request.POST.get('key', 0)
        behaviour = request.POST.get('behaviour', 0)  # TODO make this work lol

        if import_type == 0:
            importFRC.import_district(key)
        elif import_type == 1:
            importFRC.import_event(key)
        elif import_type == 3:
            importFRC.import_team(key)

    return HttpResponseRedirect(reverse_lazy('entry:import'))


@login_required(login_url='entry:login')
def logout(request):
    auth.logout(request)
    print("request.user.is_authenticated:" + str(request.user.is_authenticated))
    return HttpResponseRedirect(reverse_lazy('entry:index'))


def register_user(request):
    if request.method == 'GET':
        template = loader.get_template('entry/register.html')
        return HttpResponse(template.render({}, request))
    elif request.method == 'POST':
        username = request.POST.get('teamPosition')
        print(username)
        return HttpResponseRedirect(reverse_lazy('entry:register_user'))


@ajax
@csrf_exempt
def validate_registration(request):
    data = decode_ajax(request)
    redo, data = validate_types(request, data, False)
    return HttpResponse(dumps(redo), content_type="application/json")


@login_required(login_url='entry:login')
def admin_redirect(request, **kwargs):
    if request.user.is_superuser:
        if 'whereto' in kwargs:
            return HttpResponseRedirect(reverse_lazy('admin:index') + 'entry/' + kwargs['whereto'] + "/")

        return HttpResponseRedirect(reverse_lazy('admin:index'))
    return HttpResponseRedirect(reverse_lazy('entry:index'))


def handler404(request, exception, template_name="entry/secret.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def make_int(s):
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams(user):
    objects = Team.objects.filter(id__in=DBTools.get_event_teams(TeamSettings.objects.get(team=user.teammember.team).currentEvent.FIRST_key))
    objects = objects.order_by('number')
    return objects


def get_all_teams():
    objects = Team.objects.all()
    objects = objects.order_by('number')
    return objects


def get_all_events():
    return Event.objects.all().order_by('start')


class TeamList(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/teams.html'
    context_object_name = "team_list"
    model = Team

    def get_queryset(self):
        return get_present_teams(self.request.user)


class Import(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/import.html'
    model = Team


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
        return get_present_teams(self.request.user)


class Visualize(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/visualization.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        return get_present_teams(self.request.user)


class ScheduleView(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule_list"
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
        return get_present_teams(self.request.user)


class Experimental(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/experimental.html'


class About(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/about.html'


class Tutorial(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/tutorial.html'


class Welcome(LoginRequiredMixin, generic.TemplateView):
    template_name = 'entry/welcome.html'


class Glance(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/glance.html'
    context_object_name = "team"

    def head(self, *args, **kwargs):
        output = {
            "test": 1
        }
        response = HttpResponse(dumps(output), content_type="application/json")
        return response


class GlanceLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/glancelanding.html'

    def get_queryset(self):
        return get_present_teams(self.request.user)


class MatchData(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/matchdata.html'
    model = Match

    def get_queryset(self):
        return Match.objects.all().filter(event_id=config.get_current_event_id()).filter(
            team_ownership=self.request.user.teammember.team)


class PitData(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/pitdata.html'
    model = Pits

    def get_queryset(self):
        return Pits.objects.all().filter(event_id=config.get_current_event_id())


class Upload(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/upload.html'


class Settings(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/settings.html'

    settings_file = {}
    try:
        path = 'settings.json'
        path = os.path.join(settings.BASE_DIR, path)
        with open(path) as f:
            settings_file = json.load(f)
    except IOError:
        print("settings.json file not found")

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse_lazy('entry:settings'))
        response.set_cookie('images', request.POST.get('images', ''))
        response.set_cookie('filters', request.POST.get('filters', ''))
        response.set_cookie('districtTeams', request.POST.get('districtTeams', ''))
        response.set_cookie('tutorialCompleted', request.POST.get('tutorialCompleted', ''))
        config.set_event(request.POST.get('currentEvent', '21ONT'))

        print(self.request.user.teammember.position)

        if self.request.user.teammember.position == "LS":
            new_settings = TeamSettings()
            print("making")
            try:
                new_settings = TeamSettings.objects.get(team=self.request.user.teammember.team)
                new_settings.currentEvent = Event.objects.get(FIRST_key=request.POST.get('currentEvent', '21ONT'))

            except TeamSettings.DoesNotExist:
                new_settings.team = self.request.user.teammember.team
                new_settings.currentEvent = Event.objects.get(FIRST_key=request.POST.get('currentEvent', '21ONT'))

            except Event.DoesNotExist:
                print("User entered event that doesn't exist")
                return response

            new_settings.save()

        return response


class DBTools:

    present_team_list = None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def team_id_lookup(team_number):
        """
        :param team_number: FRC Team Number
        :type team_number: int
        :return: Team ID within the DB
        """
        team_id = Team.objects.get(number=team_number).id

        return team_id

    def get_event_teams(event_key):
        """
        :param event_key: FIRST Event Key
        :type event_key: str
        :return : List of team IDs attending said event
        :rtype : List
        """
        team_list = [0]
        event_id = Event.objects.get(FIRST_key=event_key)
        schedule_list = Schedule.objects.all().filter(event_id=event_id)

        for match in schedule_list:
            team_list.append(match.blue1)
            team_list.append(match.blue2)
            team_list.append(match.blue3)
            team_list.append(match.red1)
            team_list.append(match.red2)
            team_list.append(match.red3)

        team_list.remove(0)
        print(team_list)
        team_list.sort()
        present_team_list = team_list
        return present_team_list

    def update_event_teams(event_key):
        """
        :param event_key: FIRST Event Key
        :type event_key: str
        :return None
        """
        DBTools.get_event_teams(event_key)

    def event_id_lookup(FIRST_key):
        conn = sqlite3.connect(str(os.path.join(DBTools.BASE_DIR, "db.sqlite3")))
        c = conn.cursor()
        try:
            return c.execute('SELECT id FROM entry_event WHERE FIRST_key==?', (FIRST_key,)).fetchone()[0]
        except Exception:
            return None

    def event_key_lookup(event_id):
        conn = sqlite3.connect(str(os.path.join(DBTools.BASE_DIR, "db.sqlite3")))
        c = conn.cursor()
        try:
            return c.execute('SELECT FIRST_key FROM entry_event WHERE id==?', (event_id,)).fetchone()[0]
        except Exception:
            return None
