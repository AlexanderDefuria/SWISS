import requests
import json
import os
from apps.entry.models import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


_headers = {'Authorization': f'Basic {get_secret("FIRST_API_BASE64")}'}
_events = []
_baseUrl = 'https://frc-api.firstinspires.org/v3.0/2023/'
def getTeams(page = None, eventCode = None):
    _request = f'{_baseUrl}teams'
    if page and eventCode:
        _request += f'?page={page}&eventCode={eventCode}'
    elif eventCode:
        _request += f'?eventCode={eventCode}'
    elif page:
        _request += f'?page={page}'
    else:
        pass
    team_count = requests.get(_request, headers=_headers).json()
    return team_count

def getEvent():
    event = requests.get(f'{_baseUrl}events', headers=_headers).json()
    return event


baseTeamInfo = requests.get(f'{_baseUrl}teams', headers=_headers).json()

pageTotal = int(baseTeamInfo['pageTotal'])
event = getEvent()['Events']

def getTeamList(eventCode = None):
    for currentPage in range(1,pageTotal):
        pageInfo = getTeams(currentPage,eventCode)
        getTeamNumbers = pageInfo['teamCountPage']
        for teamIndex in range(getTeamNumbers):
            teamInfo = pageInfo['teams'][teamIndex]
            print(f"{teamInfo['nameShort']} {teamInfo['teamNumber']} located in {teamInfo['stateProv']}, {teamInfo['country']}")



for currentEvent in range(len(event)):
    eventInfo = event[currentEvent]
    _events.append(eventInfo['code'])
    print(f"{eventInfo['name']} has the first key of {eventInfo['code']}, and the district key of {eventInfo['districtCode']}, is the event type of {eventInfo['type']}, starts on {eventInfo['dateStart']}, and ends on {eventInfo['dateEnd']}")
print(_events)
print(getTeamList(eventCode="CTHAR"))


