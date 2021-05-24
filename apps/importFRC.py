import base64
from typing import overload

import requests
from apps.entry.models import *
from apps import config
import datetime

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/"
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))
header = {"Authorization": "Basic " + str(b64_token, "utf-8"),
          "Accept": "application/json"}

print(header)
print("")


def clean_key(key):
    return str(key).upper().strip()


def import_district(key=config.get_current_district_key(), year=2021):
    key = clean_key(key)
    request = "/events?districtCode=" + key
    try:
        request = get_request(request, year)
    except NoGoodResponseError:
        return
    events = request['Events']

    for event in events:
        import_event(event['code'])

    return


def import_event(key, year='2021'):
    import_event_page(key, 1, year=year)


def import_event_page(key, page, year='2021'):
    print(key)
    teams = None
    events = None

    request = "/teams?eventCode=" + key + '&page=' + str(page)
    try:
        request = get_request(request, year)
        teams = request['teams']
        if int(request['pageCurrent']) < int(request['pageTotal']):
            import_event_page(key, page + 1)
    except NoGoodResponseError:
        print("invalid teams list by eventCode")
        print(print(request))
    except KeyError:
        pass

    request = "/events?eventCode=" + key
    try:
        request = get_request(request,year)
        events = request['Events']
        if int(request['pageCurrent']) < int(request['pageTotal']):
            import_event_page(key, page + 1)
    except NoGoodResponseError:
        print("invalid events list by eventCode")
        print(print(request))
        return
    except KeyError:
        pass

    for event in events:
        new_event = Event()
        try:
            if Event.objects.get(FIRST_key=event['code']):
                new_event = Event.objects.get(FIRST_key=event['code'])
                print("Updating existing event..." + str(event['name']))
        except Event.DoesNotExist:
            print("Creating new event..." + str(event['name']))

        new_event.name = event['name']
        new_event.FIRST_key = event['code']
        print(int(event['dateStart'][5:7]))
        new_event.start = datetime.date(int(event['dateStart'][0:3]), int(event['dateStart'][5:7]), int(event['dateStart'][8:10]))
        new_event.end = datetime.date(int(event['dateEnd'][0:3]), int(event['dateEnd'][5:7]), int(event['dateEnd'][8:10]))
        new_event.FIRST_eventType = 1
        new_event.save()
        print("New EVENT:")
        print(new_event)
        print("")

    # If we're populating teams for the event then purge the existing ones otherwise ignore
    if teams is not None:
        existing = Schedule.objects.all().filter(event_id=Event.objects.get(FIRST_key=key).id)
        for each in existing:
            each.delete()

    # Populate schedule with dummies to display teams at event, not included in the schedule display frontend
    i = 0
    new_schedule = Schedule()

    if teams is None:
        return

    for team in teams:
        new_team = import_team_json(team)

        if i == 6:
            new_schedule.blue_score = 0
            new_schedule.red_score = 0
            new_schedule.match_number = 0
            new_schedule.match_type = "placeholder"
            new_schedule.placeholder = True
            print(new_schedule)
            new_schedule.save()
            new_schedule = Schedule()
            i = 0

        if i == 0:
            new_schedule.blue_score = 0
            new_schedule.red_score = 0
            new_schedule.match_number = 0
            new_schedule.match_type = "placeholder"
            new_schedule.placeholder = True
            print(new_schedule)
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.blue1 = new_team.number
        elif i == 1:
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.blue2 = new_team.number
        elif i == 2:
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.blue3 = new_team.number
        elif i == 3:
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.red1 = new_team.number
        elif i == 4:
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.red2 = new_team.number
        elif i == 5:
            new_schedule.event = Event.objects.get(FIRST_key=key)
            new_schedule.red3 = new_team.number

        i += 1

    return


def import_team(team_number, year='2021'):
    request = "/teams?teamNumber=" + str(team_number)
    try:
        request = get_request(request, year)

    except NoGoodResponseError:
        print(request)
        print("NO GOOD RESPONSE")
        return

    teams = request['teams']
    for team in teams:
        import_team_json(team)

    return


def import_team_json(json_object):
    new_team = Team()
    try:
        if Team.objects.get(number=json_object['teamNumber']):
            new_team = Team.objects.get(number=json_object['teamNumber'])
            print("Updating existing team..." + str(json_object['teamNumber']))
    except Team.DoesNotExist:
        print("Creating new team..." + str(json_object['teamNumber']))

    new_team.name = json_object['nameShort']
    new_team.number = json_object['teamNumber']
    new_team.geo_location = json_object['stateProv']
    new_team.save()
    print(new_team)

    return new_team


def import_schedule(event_slug):
    return


def get_request(request, year='2021'):

    request = str(request)

    if request[0] != "/":
        request += "/"

    if year is None:
        answer = requests.get(api_url_base, headers=header)

        # Raise error and pass over the function if the data is not cached and it is infact a good answer
        print(answer)
        if not answer.ok:
            raise NoGoodResponseError

        year = answer.json()["currentSeason"]

    answer = requests.get(api_url_base + str(year) + request, headers=header)
    if not answer.ok:
        raise NoGoodResponseError

    return answer.json()


class PresentTeams:
    present_teams = 0

    def update_present_teams(self):
        config.get_current_event_key()
        pass

    pass


# Wooooowwwww custom error handling ooooooohhhh, thanks uottawa intro to comp sci.
class NoGoodResponseError(Exception):
    pass



