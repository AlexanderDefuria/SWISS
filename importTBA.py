import tbaapiv3client as tba
from tbaapiv3client import ApiException
import sqlite3
import json
from entry import config
import datetime
import os

configuration = tba.Configuration()
configuration.api_key['X-TBA-Auth-Key'] = 'TaaEaU05CN3V89QGeDEKDSPYtfsFTAX0L8aNgAmjSAecJd2GpX4Avj5gQLjKKKls'


district_api = tba.DistrictApi(tba.ApiClient(configuration))
event_api = tba.EventApi(tba.ApiClient(configuration))
district_key = '2019ont'
event_key = config.current_event_key
event_data = []
district_teams = []


def change_district(new_district_key):
    global district_key
    district_key = new_district_key


def import_events():
    try:
        event_list = district_api.get_district_events_simple(district_key)
        # print(api_response)

        for event in event_list:

            event = clean_request(event)

            print(" ")
            print(str(event))

            event = json.loads(event)
            event_data.append(event)

            data = [(str(event["name"]), str(event["key"]), str(event["event_type"]), get_date(event["start_date"]))]

            conn = sqlite3.connect("db.sqlite3")
            c = conn.cursor()
            c.executemany("INSERT INTO entry_event VALUES (NULL,?,?,?,?)", data)
            conn.commit()

        conn.close()
        print("\nDone")

    except ApiException as e:
        conn.close()
        print("Exception when calling TBAApi->get_status: %s\n" % e)


def import_teams():
    try:
        team_list = district_api.get_district_teams_simple('2019ont')

        for team in team_list:

            team = clean_request(team)

            first_remove = str(team)[str(team).find('name'):]
            second_replace = str(team)[str(team).find('nickname'):]

            team = team.replace(first_remove, '')
            team = team + second_replace

            print(team)

            team = json.loads(team)
            district_teams.append(team)

            data = [(team["team_number"], team["nickname"], team["key"])]

            conn = sqlite3.connect("db.sqlite3")
            c = conn.cursor()
            c.executemany("INSERT INTO entry_team VALUES (NULL,?,?,0,0,0,0,0,?)", data)
            conn.commit()

            print(team)

    except ApiException as e:
        print("Exception when calling TBAApi->get_status: %s\n" % e)


def import_schedule():
    try:
        team_list = district_api.get_district_teams_simple('2019ont')

        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        write = conn.cursor()
        events = []

        for row in c.execute('SELECT TBA_key FROM entry_event WHERE id!=0'):
            #print(row[0])

            event = json.loads(clean_request(event_api.get_event_simple(row[0])))
            date = get_date(event["start_date"])
            events.append(date)

        events.sort()
        event_dates = events
        events.clear()

        for event in event_dates:
            print(event)
            events.append(c.execute('SELECT TBA_key FROM entry_event WHERE start=?', (event,)))

        print(events)


    except ApiException as e:
        print("Exception when calling TBAApi->get_status: %s\n" % e)


def clean_request(item):

    index = 0

    item = str(item)

    item = str(item).replace("datetime.date(", '"')
    item = str(item).replace(")", '"')
    item = str(item).replace("None", "NA")

    for character in str(item):
        if character == "'" or character == '"':
            try:
                if item[index - 1].isalnum() and item[index + 1].isalnum():
                    item = item[:index] + item[index:]
                else:
                    item = item[:index] + '"' + item[index+1:]
            except IndexError:
                1 + 1
        index += 1

    item = item.replace('"The Cybernauts"', ' ')

    return str(item)


def get_date(raw):

    raw = raw.split(',')

    date = datetime.date(int(raw[0]),int(raw[1]),int(raw[2]))
    print(date)
    return date


def authenticate():
    if input("Are you sure you wish to clear the database and import new? [YES I AM SURE]/[NOT SURE]") == "YES I AM SURE":
        if input("ARE YOU 100% CERTAIN? [YES I AM CERTAIN]/[NOT SURE]") == "YES I AM CERTAIN":
            if input("Password: ") == "admin2019":
                import_events()
                import_teams()
                import_schedule()


# import_events()
# import_teams()
import_schedule()
