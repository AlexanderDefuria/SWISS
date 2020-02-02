import os
import sqlite3

import requests
import json
import base64
from datetime import date

conn = sqlite3.connect("db.sqlite3")

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/2020"
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))

header = {"Authorization": "Basic " + str(b64_token, "utf-8"),
        "Accept": "application/json"}

print(header)
print("\n")

##################################################################################
# API DOCS https://frcevents2.docs.apiary.io/
##################################################################################


def import_events():
    api_url = api_url_base + "/events?districtCode=ONT"
    response = requests.get(api_url, headers=header)

    event_list = response.json()['Events']

    c = conn.cursor()

    for event in event_list:
        event = clean_request(event)
        event = json.loads(event)

        data = [(str(event["name"]), str(event["code"]), str(event["type"]),
                 getDate(event['dateStart']), getDate(event['dateEnd']))]

        c.executemany("INSERT INTO main.entry_event(name,FIRST_key,FIRST_eventType,start,end,imported)"
                      " VALUES (?,?,?,?,?,FALSE)", data)

    conn.commit()
    print("\nDone Event List")


def import_teams():
    api_url = api_url_base + "/teams?teamnumber=?districtCode=ONT"
    response = requests.get(api_url, headers=header)
    district_teams = []
    c = conn.cursor()

    for x in range(1, int(response.json()['pageTotal'])):

        print("'" + str(x) + "'")

        api_url = api_url_base + "/teams?page=2?districtCode=ONT"
        print(api_url)
        response = requests.get(api_url, headers=header)

        print(response.json())
        exit(0)

        team_list = response.json()["teams"]

        for team in team_list:

            team = clean_request(team)
            print(team)

            team = json.loads(str(team))
            district_teams.append(team)

            data = [(team["teamNumber"], team["nameShort"])]

            c.executemany("INSERT INTO entry_team(id,number,name,event_one_id,event_two_id,event_three_id,"
                          "event_four_id,event_five_id) VALUES (NULL,?,?,0,0,0,0,0)", data)
            conn.commit()


def import_schedule(conn):
    c = conn.cursor()
    events = []

    for row in c.execute('SELECT * FROM entry_event WHERE id!=0'):
        print(row)
        events.append(row)


def clean_request(item):
    index = 0

    item = str(item).replace("None", "'None'")

    for character in str(item):
        if character == "'" or character == '"':
            try:
                if item[index - 1].isalnum() and item[index + 1].isalnum():
                    item = item[:index] + item[index:]
                else:
                    item = item[:index] + '"' + item[index + 1:]
            except IndexError as e:
                e = 1
        index += 1

    # Team Names
    item = item.replace('"The Cybernauts"', ' ')
    item = item.replace('"Team 7509"', '')

    # Event Names
    item = item.replace('Thompson Recreation and Athletic Centre (TRAC" Western Road & Sarnia Road',
                        "Thompson Recreation and Athletic Centre (TRAC' Western Road & Sarnia Road")
    item = item.replace('Carleton University - Ravens" Nest',
                        "Carleton University - Ravens' Nest")
    item = item.replace('""Where\\"s Waldo?""',
                        '"Wheres Waldo?"')
    item = item.replace('""',
                        '" "')
    item = item.replace('Winona Mens" Club',
                        "Winona Mens' Club")

    return str(item)


def getDate(string):
    string = str(string)[:10]
    strings = str(string).split('-')
    output = date(int(strings[0]), int(strings[1]), int(strings[2]))
    return output


# TODO Remove the force for flush
os.system('python3 manage.py flush --noinput')
import_events()
import_teams()
