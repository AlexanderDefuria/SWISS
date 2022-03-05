import os
import ast
import re
from datetime import datetime
import json


from PIL import Image
from openpyxl import Workbook

from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template import Library, loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from apps.entry.graphing import *
from apps.entry.templatetags.common_tags import *
from apps import importFRC

register = Library


@login_required(login_url='entry:login')
def match_scout_submit(request, pk):
    if request.method == 'POST':
        team = Team.objects.get(id=pk)
        match = Match()
        match.team = team
        teamsettings = TeamSettings.objects.all().filter(team_id=request.user.teammember.team)[0]
        first_key = Event.objects.all().filter(id=make_int(teamsettings.current_event.id))[0].FIRST_key

        match.event = Event.objects.get(FIRST_key=first_key)
        match_number = request.POST.get('matchNumber', -1)
        match.match_number = match_number if match_number != '' else -1

        # PRE MATCH
        match.on_field = request.POST.get('onField', True)
        match.auto_start_x = 0#request.POST.get('coordinate_x', 0.0)
        match.auto_start_y = 0#request.POST.get('coordinate_y', 0.0)
        match.preloaded_balls = request.POST.get('preloadedBalls', 1)

        # AUTO
        match.auto_route = request.POST.get('autoRoute', 0)
        match.baseline = request.POST.get('baseline', False)
        match.upper_auto = request.POST.get('upper_auto', 0)
        match.lower_auto = request.POST.get('lower_auto', 0)
        match.missed_auto = request.POST.get('missed_balls_auto', 0)
        match.auto_fouls = 0 # request.POST.get('auto_fouls', '')
        match.auto_comment = request.POST.get('auto_comment', '')

        # TELEOP
        match.lower = request.POST.get('lower', 0)
        match.upper = request.POST.get('upper', 0)
        match.missed_balls_auto = request.POST.get('missed_balls', 0)
        match.intake_type = request.POST.get('intakeType', 0)
        match.under_defense = request.POST.get('under_defense', 0)
        try:
            match.defended_by = int(request.POST.get('defended_by', '0'))
        except:
            match.defended_by = request.POST.get('defended_by', 0)
        match.offensive_fouls = request.POST.get('offensive_fouls', 0)

        # DEFENSE
        match.defense_played = request.POST.get('playedDefense', False)
        match.defense_time = 0 #request.POST.get('defense_time', 0)
        match.defense_rating = request.POST.get('defense_rating', 0)
        team_defended = request.POST.get('team_defended', 0)
        match.team_defended = team_defended if team_defended != '' else -1
        match.defense_fouls = request.POST.get('defenseFouls', 0)
        match.able_to_push = request.POST.get('pushRating', 0)

        # CLIMB
        match.lock_status = request.POST.get('lock_status', 0)
        match.endgame_action = request.POST.get('endgame_action', 0)
        match.climb_time = 0 #request.POST.get('climb_time', 0)
        match.climb_attempts = make_int(request.POST.get('climb_attempts', 0))
        match.climb_comments = request.POST.get('climb_comments', 0)

        # COMMENTS AND RANDOM IDEAS
        match.fouls_hp = request.POST.get('humanFouls', 0)
        match.fouls_driver = request.POST.get('driverFouls', 0)
        match.yellow_card = True if request.POST.get('cardFouls', '') != '' else False

        match.scouter_name = request.user.username
        match.comment = request.POST.get('comment', '')
        match.team_ownership = request.user.teammember.team

        #print(match.get_deferred_fields())

        try:
            match.save()
            print('Success')
        except Exception as e:
            print(e)

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

    teamsettings = TeamSettings.objects.all().filter(team_id=request.user.teammember.team)[0]

    if Match.objects.filter(team_id=pk, event_id=teamsettings.current_event,
                            match_number=data['matchNumber'][0]).exists():
        # Check if there are already 6 teams that have played this match
        if Match.objects.filter(match_number=data['matchNumber'][0]).count() <= 6:
            redo['matchNumber'] = True

    return HttpResponse(json.dumps(redo), content_type="application/json")


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
        print("FIELD: " + field)

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

        print("type")
        print(type(data[field][0]))
        print(type(reqfields[field]))
        redo[field] = False if (isinstance(data[field][0], type(reqfields[field]))) else True

    for field in request.POST:
        try:
            redo[field] = not is_ascii(request.POST.get(field))
            print(request.POST.get(field))

        except AttributeError:
            print('issue')
    if request.path.__contains__("scout") and data['scouterName'][0] == '':
        redo['scouterName'] = True

    print(redo.keys())
    print(redo.values())

    return redo, data


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


@login_required(login_url='entry:login')
def pit_scout_submit(request, pk):
    if request.method == 'POST':
        team = Team.objects.get(id=pk)
        pits = Pits()
        pits.team = team
        teamsettings = TeamSettings.objects.all().filter(team_id=request.user.teammember.team)[0]
        first_key = Event.objects.all().filter(id=make_int(teamsettings.current_event.id))[0].FIRST_key

        pits.event = Event.objects.get(FIRST_key=first_key)
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
    return HttpResponse(json.dumps(redo), content_type="application/json")


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
@login_required(login_url='entry:login')
def update_glance(request, pk):
    matches = Match.objects.filter(team_id=pk, team_ownership_id=request.user.teammember.team_id).order_by(
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
            'glance_' + str(pk) + '_' + str(count) + '_' + str(datetime.datetime.now()) + '.json', f)
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


# @user_passes_test(scout_lead_check, login_url='entry:login')
@login_required(login_url='entry:login')
def download(request):
    # TODO find a way to prevent spamming this.

    path = 'match_history.xlsx'
    path = os.path.join(settings.BASE_DIR, path)
    update_csv(request.user.teammember.team_id)

    if request.method == "GET" and os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/xlsx")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response

    return Http404


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def get_csv_ajax(request):
    path = 'match_history.xlsx'
    path = os.path.join(settings.BASE_DIR, path)
    update_csv(request.user.teammember.team_id)

    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/xlsx")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response
    return Http404


def update_csv(team_id):
    print("Updating XLSX File")

    workbook = Workbook()
    writable_models = [Match, Pits]

    for model in writable_models:
        workbook.create_sheet(title=model._meta.model_name)
        sheet = workbook.get_sheet_by_name(model._meta.model_name)
        headers = model._meta.get_fields()
        x = 1
        for header in headers:
            sheet.cell(column=x, row=1, value=str(header))
            x += 1
        data = model.objects.all().values_list()
        x = 1
        y = 2
        for entry in data:
            for field in entry:
                sheet.cell(column=x, row=y, value=str(field))
                x += 1
            y += 1

    workbook.remove_sheet(workbook.get_sheet_by_name("Sheet"))
    workbook.save("match_history.xlsx")


@login_required(login_url='entry:login')
def write_image_upload(request):
    if request.method == 'POST':
        team_number = make_int(request.POST.get('teamNumber', 0))
        team = Team.objects.get(number=team_number)

        request.session.set_test_cookie()

        files = request.FILES
        files = files.popitem()[1]

        for file in files:
            file.name = str(team_number) + "-----" + str(datetime.datetime.now()).replace('.', '') + '.jpg'
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
    if request.method == 'GET':
        template = loader.get_template('entry/login.html')

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        return HttpResponse(template.render({}, request))

    elif request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
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
        year = request.POST.get('year', 0)

        if year == 0:
            year = None

        if import_type == 0:
            importFRC.import_district(key, year)
        elif import_type == 1:
            importFRC.import_event(key, year)
        elif import_type == 3:
            importFRC.import_team(key, year)

    return HttpResponseRedirect(reverse_lazy('entry:import'))


@login_required(login_url='entry:login')
def logout(request):
    auth.logout(request)
    print("request.user.is_authenticated:" + str(request.user.is_authenticated))
    return HttpResponseRedirect(reverse_lazy('entry:index'))


@ajax
@csrf_exempt
def validate_registration(request):
    data = decode_ajax(request)
    redo, data = validate_types(request, data, False)

    print("redo")
    print(redo)
    print("data")
    print(data)
    print(data['email'][0])
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(data['email'][0])):
        if len(str(data['email'][0]).strip(" ")) != 0:
            redo['email'] = True
    if len(str(data['username'])) < 5:
        redo['username'] = True
    if len(str(data['password'])) < 5:
        redo['password'] = True
    if data['password'] != data['password_validate']:
        redo['password'] = True
        redo['password_validate'] = True
    if len(str(data['team_reg_id']).strip(" ")) != 10:  # len==10 because the uuid is 6 + 4 for ['uuidxx']
        redo['team_reg_id'] = True

    return HttpResponse(json.dumps(redo), content_type="application/json")


@login_required(login_url='entry:login')
def admin_redirect(request, **kwargs):
    if request.user.is_staff:
        if 'whereto' in kwargs:
            return HttpResponseRedirect(reverse_lazy('admin:index') + 'entry/' + kwargs['whereto'] + "/")

        return HttpResponseRedirect(reverse_lazy('admin:index'))
    return HttpResponseRedirect(reverse_lazy('entry:index'))


def handler404(request, exception, template_name="entry/secret.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def make_int(s):
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams(user):
    # TODO This NEEDS to be faster
    try:
        objects = Team.objects.filter(number__in=
        get_event_teams(
            TeamSettings.objects.get(team=user.teammember.team).
                current_event.FIRST_key))
        return objects
    except TeamSettings.DoesNotExist:

        return Team.objects.all()


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
    team_list.remove(0)
    team_list.sort()
    present_team_list = team_list
    return present_team_list


def get_all_teams():
    objects = Team.objects.all()
    objects = objects.order_by('number')
    return objects


def get_all_events():
    return Event.objects.all().order_by('start')


def handle_query_present_teams(view):
    teams = get_present_teams(view.request.user)
    if teams.count() == 1 and teams.first() == Team.objects.first():
        return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

    return teams


class TeamSettingsNotFoundError(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/team_settings_not_found_error.html'


class TeamList(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/teams.html'
    context_object_name = "team_list"
    model = Team

    def get_queryset(self):
        teams = get_present_teams(self.request.user)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return teams


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
        teams = get_present_teams(self.request.user)
        print(teams)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return teams


class Visualize(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/visualization.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        teams = get_present_teams(self.request.user)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return teams


class ScheduleView(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule_list"
    model = Schedule

    def get_queryset(self):
        try:
            teamsettings = TeamSettings.objects.all().filter(team_id=self.request.user.teammember.team)[0]
        except IndexError as e:
            print(str(e) + ": There are no team settings for this query.")
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return Schedule.objects.filter(event_id=teamsettings.current_event).order_by("match_type")


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
        teams = get_present_teams(self.request.user)
        if teams.count() == 1 and teams.first() == Team.objects.first():
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return teams


class Experimental(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/experimental.html'


class About(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/about.html'


class Tutorial(generic.TemplateView):
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
        response = HttpResponse(json.dumps(output), content_type="application/json")
        return response


class GlanceLanding(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/glancelanding.html'

    def get_queryset(self):
        return handle_query_present_teams(self)


class Registration(generic.TemplateView):
    model = Team
    template_name = 'entry/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:index'))
        else:
            return super(Registration, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = User()

        if request.POST.get('team_number'):
            user.teammember = TeamMember()
            user.teammember.team = Team.objects.get(id=make_int(request.POST.get('team_number')))
            if request.POST.get('team_reg_id')[:6] != str(user.teammember.team.reg_id)[:6]:
                return HttpResponse(reverse_lazy('entry:register'))
            user.save()
            user.teammember.save()

        if request.POST.get('password') == request.POST.get('password_validate'):
            user.set_password(request.POST.get('password'))
        else:
            return HttpResponse(reverse_lazy('entry:register'))

        if request.POST.get('username') == "":
            return HttpResponse(reverse_lazy('entry:register'))

        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user.save()

        return HttpResponseRedirect(reverse_lazy('entry:update_fields'))


class MatchData(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/matchdata.html'
    model = Match

    def get_queryset(self):
        try:
            teamsettings = TeamSettings.objects.all().filter(team_id=self.request.user.teammember.team)[0]
        except IndexError:
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return Match.objects.all().filter(event_id=teamsettings.current_event).filter(
            team_ownership=self.request.user.teammember.team.id)


class PitData(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/pitdata.html'
    model = Pits

    def get_queryset(self):
        try:
            teamsettings = TeamSettings.objects.all().filter(team_id=self.request.user.teammember.team)[0]
        except IndexError:
            return HttpResponseRedirect(reverse_lazy('entry:team_settings_not_found_error'))

        return Pits.objects.all().filter(event_id=teamsettings.current_event).filter(
            team_ownership=self.request.user.teammember.team.id)


class Upload(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/upload.html'


class Settings(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/settings.html'

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse_lazy('entry:settings'))
        response.set_cookie('images', request.POST.get('images', ''))
        response.set_cookie('filters', request.POST.get('filters', ''))
        response.set_cookie('districtTeams', request.POST.get('districtTeams', ''))
        response.set_cookie('tutorialCompleted', request.POST.get('tutorialCompleted', ''))
        response.set_cookie('teamsBehaviour', request.POST.get('teamsBehaviour', ''))

        if self.request.user.teammember.position == "LS":
            new_settings = TeamSettings()
            print("making")
            try:
                new_settings = TeamSettings.objects.get(team=self.request.user.teammember.team)
                new_settings.current_event = Event.objects.get(FIRST_key=request.POST.get('currentEvent', '21ONT'))

            except TeamSettings.DoesNotExist:
                new_settings.team = self.request.user.teammember.team
                new_settings.current_event = Event.objects.get(FIRST_key=request.POST.get('currentEvent', '21ONT'))

            except Event.DoesNotExist:
                print("User entered event that doesn't exist")
                return response

            new_settings.save()

        return response
