import base64
import requests
from apps.entry.models import *

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/"
year = None
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))
header = {"Authorization": "Basic " + str(b64_token, "utf-8"),
          "Accept": "application/json"}

print(header)
print("")


def import_district(key):
    return


def import_event(key):

    return


def import_team(team_number):
    return


def import_schedule(event_slug):
    return


def get_request(request):
    global year

    if year is None:
        year = requests.get(api_url_base, headers=header).json()["currentSeason"]

    return requests.get(api_url_base + str(year) + request, headers=header).json()



print(get_request(""))