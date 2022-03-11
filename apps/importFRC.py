import base64
from typing import overload

import requests
from apps.entry.models import *
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


def import_district(key, year='2022'):
    key = clean_key(key)
    if year is None or year == "":
        year = '2022'
    request = "/events?districtCode=" + key
    try:
        request = get_request(request, year)
    except NoGoodResponseError:
        return
    events = request['Events']

    for event in events:
        import_event(event['code'], year)

    return


def import_event(key, year='2022'):
    import_event_page(key, 1, year=year)


def import_event_page(key, page, year='2022'):
    print(key)
    teams = None
    events = None

    request = "/teams?eventCode=" + key + '&page=' + str(page)
    try:
        request = get_request(request, year)
        teams = request['teams']
        if int(request['pageCurrent']) < int(request['pageTotal']):
            import_event_page(key, page + 1, year)
    except NoGoodResponseError:
        print("invalid teams list by eventCode")
        print(print(request))
    except KeyError:
        pass

    request = "/events?eventCode=" + key
    try:
        request = get_request(request, year)
        events = request['Events']
        if int(request['pageCurrent']) < int(request['pageTotal']):
            import_event_page(key, page + 1, year)
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
        try:
            new_event.FIRST_district_key = event['districtCode']
        except Exception as e:
            print(e)
            new_event.FIRST_key = "Regional"

        print((event['dateStart']))
        new_event.start = datetime.date(int(event['dateStart'][0:3]), int(event['dateStart'][5:7]),
                                        int(event['dateStart'][8:10]))
        new_event.end = datetime.date(int(event['dateEnd'][0:3]), int(event['dateEnd'][5:7]),
                                      int(event['dateEnd'][8:10]))
        new_event.FIRST_eventType = event['type']
        new_event.save()
        print("New EVENT:")
        print(new_event)
        print("")

    # If we're populating teams for the event then purge the existing ones otherwise ignore
    if teams is not None:
        try:
            existing = Schedule.objects.all().filter(event_id=Event.objects.get(FIRST_key=key).id)
            for each in existing:
                each.delete()
        except Event.DoesNotExist:
            NoGoodResponseError

    if teams is None:
        return

    # Populate schedule with dummies to display teams at event, not included in the schedule display frontend
    for team in teams:
        new_team = import_team_json(team)

        new_schedule = Schedule()

        new_schedule.blue_score = 0
        new_schedule.red_score = 0
        new_schedule.match_number = 0
        new_schedule.match_type = "placeholder"
        new_schedule.placeholder = True
        new_schedule.event = Event.objects.get(FIRST_key=key)
        # TODO Fix this hackish solution.
        #                    vvvvvvvvvvvv
        new_schedule.red1 = new_team.number
        new_schedule.red2 = new_team.number
        new_schedule.red3 = new_team.number
        new_schedule.blue1 = new_team.number
        new_schedule.blue2 = new_team.number
        new_schedule.blue3 = new_team.number
        new_schedule.save()

    return


def import_team(team_number, year='2022'):
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
    new_team.id = new_team.number
    new_team.save()
    print(new_team)

    return new_team


def import_schedule(event_key, year="2022", playoffs=False):
    event_key = clean_key(event_key)
    if year is None or year == "":
        year = '2022'
    request = "/schedule/" + event_key + "?tournamentLevel=" + ("Playoff" if playoffs else "Qualification")
    try:
        request = get_request(request, year)
    except NoGoodResponseError:
        print(request)
        print("NO GOOD RESPONSE")
        return

    if not Event.objects.get(FIRST_key=event_key):
        import_event(event_key, year)

    matches = request['Schedule']
    for match in matches:
        import_schedule_json(match, event_key, playoffs)
    print(request)

    return


def import_schedule_json(json_object, event_key, playoffs=False):
    new_schedule = Schedule()

    print(json_object)
    try:
        if Schedule.objects.get(match_number=json_object['matchNumber'], match_type=("Playoff" if playoffs else "Qualification"), event_id=Event.objects.get(FIRST_key=event_key)):
            new_schedule = Schedule.objects.get(match_number=json_object['matchNumber'], match_type=("Playoff" if playoffs else "Qualification"), event_id=Event.objects.get(FIRST_key=event_key))
            print("Updating existing schedule entry..." + str(json_object['matchNumber']))
    except Schedule.DoesNotExist:
        print("Creating new schedule entry... Match:" + str(json_object['matchNumber']))
        new_schedule.event_id=Event.objects.get(FIRST_key=event_key).id

    new_schedule.match_number = json_object['matchNumber']
    new_schedule.match_type = json_object['tournamentLevel']
    new_schedule.description = json_object['description']
    new_schedule.placeholder = False
    new_schedule.red_score = 0
    new_schedule.blue_score = 0

    new_schedule.red1 = json_object['teams'][0]['teamNumber']
    new_schedule.red2 = json_object['teams'][1]['teamNumber']
    new_schedule.red3 = json_object['teams'][2]['teamNumber']
    new_schedule.blue1 = json_object['teams'][3]['teamNumber']
    new_schedule.blue2 = json_object['teams'][4]['teamNumber']
    new_schedule.blue3 = json_object['teams'][5]['teamNumber']

    new_schedule.save()
    print(new_schedule)

    return new_schedule


def get_request(request, year='2022'):
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
        print(api_url_base + str(year) + request)
        raise NoGoodResponseError
    print(api_url_base + str(year) + request)

    return answer.json()


class NoGoodResponseError(Exception):
    pass


#import_schedule("ON306")