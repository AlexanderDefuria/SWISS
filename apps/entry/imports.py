import datetime

import requests
from apps.entry.models import Team, Event
from utils import get_secret

_headers = {'Authorization': f'Basic {get_secret("FIRST_API_BASE64")}'}
_events = []
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


def get_team_list(event_code=None):
    base_team_info = requests.get(f'{_baseUrl}teams', headers=_headers).json()
    page_total = int(base_team_info['pageTotal'])

    for current_page in range(1, page_total):
        page_info = get_teams(current_page, event_code)
        getTeamNumbers = page_info['teamCountPage']


        for team_index in range(getTeamNumbers):
            team_info = page_info['teams'][team_index]
            teamExists = Team.objects.filter(id=team_info['teamNumber']).exists()
            if teamExists:
                currTeam = Team.objects.get(id=team_info['teamNumber'])
            else:
                currTeam = Team()

            currTeam.number = team_info['teamNumber']
            currTeam.id = team_info['teamNumber']
            currTeam.name = team_info['nameShort']
            currTeam.colour = '#000000'
            currTeam.pick_status = 0


            # print(currTeam)

            currTeam.save()

            # # print(f"{team_info['nameShort']} {team_info['teamNumber']} located "
            #       f"in {team_info['stateProv']}, {team_info['country']}")

            new_team: Team
            try:
                new_team = Team.objects.get(pk=team_info['teamNumber'])
            except Team.DoesNotExist:
                new_team = Team()
            new_team.number = team_info['teamNumber']
            new_team.name = team_info['nameShort']
            new_team.id = new_team.number
            new_team.save()

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
                # print(f"{currentTeam} image data is {currentImage}")
            team_image.save()
def import_first():
    event = get_all_events()['Events']

    for currentEvent in range(len(event)):
        eventInfo = event[currentEvent]
        _events.append(eventInfo['code'])

        eventExists = Event.objects.filter(name=eventInfo['name']).exists()

        if eventExists:
            theEvent = Event.objects.get(name=eventInfo['name'])
        else:
            theEvent = Event()

        theEvent.name = eventInfo['name']
        theEvent.FIRST_key = eventInfo['code']
        theEvent.FIRST_eventType = eventInfo['type']
        theEvent.start = datetime.datetime.now()
        theEvent.end = datetime.datetime.now()
        theEvent.imported = True

        theEvent.save()
        # print(theEvent)

        # print(f"{eventInfo['name']} has the first key of {eventInfo['code']}, and the district "
        #       f"key of {eventInfo['districtCode']}, is the event type of {eventInfo['type']},"
        #       f" starts on {eventInfo['dateStart']}, and ends on {eventInfo['dateEnd']}")

    # print(_events)
    # print(get_team_list(event_code="CTHAR"))
