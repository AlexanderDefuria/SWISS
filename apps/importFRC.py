import base64
import requests
from apps.entry.models import *
from apps import config
import datetime

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/"
year = None
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))
header = {"Authorization": "Basic " + str(b64_token, "utf-8"),
          "Accept": "application/json"}

print(header)
print("")


def import_district():
    return import_district(key=config.get_current_district_key())


def import_district(key):
    request = "/events?districtCode=" + key
    request = get_request(request)
    events = request['Events']

    for event in events:
        import_event(event['code'])

    return


def import_event(key):
    request = "/teams?eventCode=" + key
    request = get_request(request)
    teams = request['teams']

    request = "/events?eventCode=" + key
    request = get_request(request)
    events = request['Events']

    for event in events:
        new_event = Event()
        new_event.name = event['name']
        new_event.FIRST_key = event['code']
        new_event.start = datetime.date(event['dateStart'][0:3], event['dateStart'][5:6], event['dateStart'][8:9])
        new_event.end = datetime.date(event['dateEnd'][0:3], event['dateEnd'][5:6], event['dateEnd'][8:9])
        new_event.FIRST_eventType = 1
        new_event.save()

    for team in teams:
        import_team_json(team)

    return


def import_team(team_number):
    request = "/teams?teamNumber=" + str(team_number)
    request = get_request(request)
    teams = request['teams']
    for team in teams:
        import_team_json(team)

    return


def import_team_json(json_object):
    new_team = Team()
    new_team.name = json_object['nameShort']
    new_team.number = json_object['teamNumber']
    new_team.geo_location = json_object['stateProv']
    new_team.save()


def import_schedule(event_slug):
    return


def get_request(request):
    global year

    request = str(request)

    if request[0] != "/":
        request += "/"

    if year is None:
        year = requests.get(api_url_base, headers=header).json()["currentSeason"]

    return requests.get(api_url_base + str(year) + request, headers=header).json()



