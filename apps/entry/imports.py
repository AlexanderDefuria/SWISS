import datetime
import traceback

import requests
from apps.entry.models import Team, Event
from utils import get_secret

_headers = {'Authorization': f'Basic {get_secret("FIRST_API_BASE64")}'}
events = []
_baseUrl = 'https://frc-api.firstinspires.org/v3.0/2022/'


def make_request(request: str):
    response = requests.get(request, headers=_headers)
    if response.status_code != 200:
        raise Exception(f'FIRST API returned {response.status_code}')
    return response


def get_teams(page=None, event_code=None):
    request = f'{_baseUrl}teams'
    if page and event_code:
        request += f'?page={page}&eventCode={event_code}'
    elif event_code:
        request += f'?eventCode={event_code}'
    elif page:
        request += f'?page={page}'

    team_count = make_request(request).json()
    return team_count


def get_all_events() -> dict:
    events_json = make_request(f'{_baseUrl}events').json()
    if type(events_json) is not dict:
        print(events_json)
        raise Exception('FIRST API returned invalid data')
    return events_json


def get_single_event(event_code: str):
    return make_request(f'{_baseUrl}events?eventCode={event_code}').json()


def get_events(event_code: str = None):
    if event_code:
        _events = get_single_event(event_code)['Events']
    else:
        _events = get_all_events()['Events']

    print(_events)

    for event_info in _events:
        if type(event_info) is not dict:
            continue

        _events.append(event_info['code'])

        eventExists = Event.objects.filter(FIRST_key=event_info['code']).exists()

        if eventExists:
            theEvent = Event.objects.get(FIRST_key=event_info['code'])
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
        base_team_info = make_request(f'{_baseUrl}teams?teamNumber={team_number}').json()
    else:
        base_team_info = make_request(f'{_baseUrl}teams').json()

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
def calculate_WinLoss(team: Team):
    try:
        team.winRate = (team.totalMatchesWon / team.totalMatchesPlayed) * 100
        team.save()
    except:
        print("Error, team not in database")

    return

def get_team_logos():
    base_team_logo_info = make_request(f'{_baseUrl}avatars').json()

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
def get_match_data():
    for event in Event.objects.all():

        try:
            base_data = make_request(f'{_baseUrl}matches/{event.FIRST_key}?tournamentLevel=Qualification').json()
            base_data = base_data['Matches']
            number_of_matches = len(base_data)
            for match in range(number_of_matches):

                current_match = base_data[match]
                if current_match["scoreRedFinal"] > current_match["scoreBlueFinal"]:
                    winner = "R"
                elif current_match["scoreRedFinal"] < current_match["scoreBlueFinal"]:
                    winner = "B"

                for team in current_match["teams"]:
                    team_number = team["teamNumber"]
                    team_info = Team.objects.get(id=team_number)

                    if team["station"][0] == winner:
                        team_info.totalMatchesWon += 1
                        # team_info.totalMatchesWon = 0
                        # team_info.totalMatchesLost = 0
                        # team_info.totalMatchesPlayed = 0
                        # print(f'{team["teamNumber"]} won')
                    else:
                        # team_info.totalMatchesWon = 0
                        # team_info.totalMatchesLost = 0
                        # team_info.totalMatchesPlayed = 0
                        team_info.totalMatchesLost += 1
                        # print(f'{team["teamNumber"]} lost')

                    team_info.totalMatchesPlayed += 1

                    calculate_WinLoss(team_number)
        except:
            print(f"data missing for {event.FIRST_key}")

        print(event)





            # print(f"Match Number is {current_match['matchNumber']} Video Link is {current_match['matchVideoLink']} Reds score was {current_match['scoreRedFinal']} Blues score was {current_match['scoreBlueFinal']} The winner was {winner}")


def import_first(event_code: str = None, team_number: int = None) -> bool:
    """
    Imports data from FIRST API
    Pass None, None to import all teams and all events
    :param event_code:
    :param team_number:
    :return:
    """
    try:
        if event_code and not team_number:
            get_events(event_code)
            get_team_list(event_code)
        elif team_number and not event_code:
            get_team_list(team_number=team_number)
            get_team_logos()
        elif event_code and team_number:
            get_team_list(event_code=event_code, team_number=team_number)
            get_team_logos()
        else:
            # get_team_logos()
            get_events()
            get_team_list()
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return False
    return True
