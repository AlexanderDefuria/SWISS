import datetime

import requests
from apps.entry.models import Team, Event
from utils import get_secret

_headers = {'Authorization': f'Basic {get_secret("FIRST_API_BASE64")}'}
events = []
_baseUrl = 'https://frc-api.firstinspires.org/v3.0/2023/'

def get_teams(page=None, event_code=None):
    request = f'{_baseUrl}teams'
    if page and event_code:
        request += f'?page={page}&eventCode={event_code}'
    elif event_code:
        request += f'?eventCode={event_code}'
    elif page:
        request += f'?page={page}'

    team_count = requests.get(request, headers=_headers).json()
    return team_count


def get_all_events():
    return requests.get(f'{_baseUrl}events', headers=_headers).json()


def get_single_event(event_code: str):
    return requests.get(f'{_baseUrl}events?eventCode={event_code}', headers=_headers).json()


def get_events(event_code: str):
    if event_code:
        _events = get_single_event(event_code)['Events']
    else:
        _events = get_all_events()['Events']

    for event_info in _events:
        _events.append(event_info['code'])

        eventExists = Event.objects.filter(name=event_info['name']).exists()

        if eventExists:
            theEvent = Event.objects.get(name=event_info['name'])
        else:
            theEvent = Event()

        theEvent.name = event_info['name']
        theEvent.FIRST_key = event_info['code']
        theEvent.FIRST_eventType = event_info['type']
        theEvent.start = datetime.datetime.now()
        theEvent.end = datetime.datetime.now()
        theEvent.imported = True

        theEvent.save()


def get_team_list(event_code: str = None, team_number: int = None):
    if team_number:
        base_team_info = requests.get(f'{_baseUrl}teams?teamNumber={team_number}', headers=_headers).json()
    else:
        base_team_info = requests.get(f'{_baseUrl}teams', headers=_headers).json()

    page_total = int(base_team_info['pageTotal'])

    for current_page in range(1, page_total):
        page_info = get_teams(current_page, event_code)
        getTeamNumbers = page_info['teamCountPage']
        for team_index in range(getTeamNumbers):
            team_info = page_info['teams'][team_index]

            team: Team
            try:
                team = Team.objects.get(pk=team_info['teamNumber'])
            except Team.DoesNotExist:
                team = Team()
            team.number = team_info['teamNumber']
            team.name = team_info['nameShort']
            team.colour = '#000000'
            team.id = team.number
            team.pick_status = 0
            team.save()

def get_team_logos():
    base_team_logo_info = requests.get(f'{_baseUrl}avatars', headers=_headers).json()
    for currentPage in range(base_team_logo_info["pageTotal"]):
        teams_on_page = base_team_logo_info["teamCountPage"]
        for teamSelected in range(teams_on_page):
            image_data = base_team_logo_info["teams"][teamSelected]
            if len(image_data['encodedAvatar']) < 1:
                team_image = Team.objects.get(id=image_data['teamNumber'])
                team_image.avatar = "NA"
            else:
                team_image = Team.objects.get(id=image_data['teamNumber'])
                team_image.avatar = image_data["encodedAvatar"]
                currentTeam = image_data["teamNumber"]
                currentImage = image_data["encodedAvatar"]
            team_image.save()


def import_first(event_code: str = None, team_number: int = None):
    """
    Imports data from FIRST API
    Pass None, None to import all teams and all events
    :param event_code:
    :param team_number:
    :return:
    """
    get_events(event_code)
    get_team_list(event_code, team_number)

