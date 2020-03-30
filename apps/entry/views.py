import base64
import csv
import os
import dbTools

from datetime import datetime
from json import dumps

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template import Library, loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test

from apps.entry.graphing import *
from apps.entry.models import Team, Match, Schedule, Images

register = Library


@login_required(login_url='entry:login')
def write_teleop(request, pk):
    print("Adding teleop phase to database")
    if request.method == 'POST':

        team = Team.objects.get(id=pk)
        match = Match.objects.filter(team_id=team.id).latest('match_number')

        print(team)
        print(request.POST)

        print('Success')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


@login_required(login_url='entry:login')
def write_auto(request, pk):
    print("Adding auto phase to database")
    if request.method == 'POST':
        team = Team.objects.get(id=pk)

        # Match Setup
        match = Match()
        match.match_number = make_int(request.POST.get('MatchNumber', 0))
        match.event_id = config.current_event_id
        if match.event_id != config.current_event_id:
            raise Http404
        match.team_id = team.id

        return HttpResponseRedirect('/entry/' + str(pk) + '/teleop/' + str(match.match_number))

    else:
        print('Fail')
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


def view_matches(request):
    if request.method == 'GET':
        print("POSTED")
    return HttpResponseRedirect(reverse_lazy('visualize'))


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def update_graph(request):
    data = decode_ajax(request)
    create_teams_graph(data)

    try:
        image_data = base64.b64encode(open(str(settings.BASE_DIR) + "/media/dynamic_plot.png", "rb").read())
        return HttpResponse(image_data, content_type="image/png")
    except IOError:
        print("Image not found")
        return Http404


@ajax
@csrf_exempt
@login_required(login_url='entry:login')
def validate_match(request, pk):
    # The parsing of the db to check if a team has played at a particular match already is done server side
    # The ajax post sends only the match number in a JSON file to comply with AJAX datatype specification
    # dumps() is to convert dictionary into JSON format for HttpResponse to keep it simple stupid

    data = decode_ajax(request)['match_number']
    provided_match_number = make_int(data[0])
    result = {'result': False}

    if not Match.objects.filter(team_id=pk, event_id=config.get_current_event_key(),
                                match_number=provided_match_number).exists():
        if Match.objects.filter(match_number=provided_match_number).count() < 6:
            result['result'] = True

    return HttpResponse(dumps(result), content_type="application/json")


@login_required(login_url='entry:login')
def decode_ajax(request):
    return dict(QueryDict(request.body.decode()))


def scout_lead_check(user):
    return user.groups.filter(name="Scouting").exists()


# TODO Export into .xls instead of .csv
@user_passes_test(scout_lead_check, login_url='entry:login')
@login_required(login_url='entry:login')
def download(request):
    redirect_field_name = 'entry:login'
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
        print("COOKIES???: " + str(request.session.test_cookie_worked()))

        files = request.FILES
        files = files.popitem()[1]

        for file in files:
            file.name = str(team_number) + "-----" + str(datetime.now()).replace('.', '')
            image = Images(name=team.name, image=file)
            image.save()
            team.images.add(image)
            team.save()
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))
    else:
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


@login_required(login_url='entry:login')
def write_pit_upload(request):
    if request.method == 'POST':
        team_number = 0
    else:
        return HttpResponseRedirect(reverse_lazy('entry:team_list'))


def login(request):
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

        return HttpResponseRedirect(reverse_lazy('entry:team_list'))

    return HttpResponseRedirect(reverse_lazy('entry:login'))


@login_required(login_url='entry:login')
def logout(request):
    auth.logout(request)
    print("request.user.is_authenticated:" + str(request.user.is_authenticated))
    return HttpResponseRedirect(reverse_lazy('entry:team_list'))


def make_int(s):
    s = str(s)
    s = s.strip()
    return int(s) if s else 0


def get_present_teams():
    event_key = config.get_current_event_key()
    objects = Team.objects.filter(number__in=dbTools.get_event_teams(event_key))
    objects = objects.order_by('number')
    return objects


class TeamNumberList(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/landing.html'
    context_object_name = "team_list"
    model = Team

    def get_queryset(self):
        return get_present_teams()


class Auto(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/auto.html'


class Teleop(LoginRequiredMixin, generic.DetailView):
    login_url = 'entry:login'
    model = Team
    template_name = 'entry/teleop.html'


class Visualize(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/visualize.html'


class ImageUpload(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'entry/image-upload.html'
    model = Team
    context_object_name = "team_list"


class ImageViewer(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/image-viewer.html'
    model = Team
    context_object_name = "team_list"

    def get_queryset(self):
        return get_present_teams()


class ScheduleView(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule"
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(event_id=config.current_event_id).order_by("match_type")


class PitUpload(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'entry/schedule.html'
    context_object_name = "schedule"
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(event_id=config.current_event_id).order_by("match_type")
