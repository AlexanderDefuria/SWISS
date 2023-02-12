import requests
from apps.entry.models import Team
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
            print(f"{team_info['nameShort']} {team_info['teamNumber']} located "
                  f"in {team_info['stateProv']}, {team_info['country']}")

            new_team: Team
            try:
                new_team = Team.objects.get(pk=team_info['teamNumber'])
            except Team.DoesNotExist:
                new_team = Team()
            new_team.number = team_info['teamNumber']
            new_team.name = team_info['nameShort']
            new_team.id = new_team.number
            new_team.save()


def import_first(event_code: str = None, team_number: int = None):
    if event_code:
        _events = get_single_event(event_code)['Events']
    else:
        _events = get_all_events(team_number=team_number)['Events']

    for event_info in _events:
        events.append(event_info['code'])
        print(f"{event_info['name']} has the first key of {event_info['code']}, and the district "
              f"key of {event_info['districtCode']}, is the event type of {event_info['type']},"
              f" starts on {event_info['dateStart']}, and ends on {event_info['dateEnd']}")
