import os
import sqlite3

import requests
import json
import base64
from datetime import date

import dbTools
from apps import config

conn = sqlite3.connect("db.sqlite3")

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/2020"
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))

header = {"Authorization": "Basic " + str(b64_token, "utf-8"),
        "Accept": "application/json"}

print(header)
print("")


##################################################################################
# API DOCS https://frcevents2.docs.apiary.io/
##################################################################################


def import_events():
    print("Importing Events...")

    api_url = api_url_base + "/events?districtCode=" + config.get_current_district_key()
    response = requests.get(api_url, headers=header)

    event_list = response.json()['Events']

    c = conn.cursor()

    for event in event_list:
        event = clean_request(event)
        event = json.loads(event)

        data = [(str(event["name"]), str(event["code"]), str(event["type"]),
                 get_date(event['dateStart']), get_date(event['dateEnd']))]

        c.executemany("INSERT INTO main.entry_event(name,FIRST_key,FIRST_eventType,start,end,imported)"
                      " VALUES (?,?,?,?,?,FALSE)", data)

    conn.commit()
    print("Done.")


def import_teams():
    print("Importing Teams...")

    api_url = api_url_base + "/teams?districtCode=" + config.get_current_district_key()
    response = requests.get(api_url, headers=header)
    district_teams = []
    c = conn.cursor()

    for x in range(1, int(response.json()['pageTotal'])):
        api_url = api_url + "&page=" + str(x)
        response = requests.get(api_url, headers=header)

        team_list = response.json()["teams"]

        for team in team_list:

            team = clean_request(team)

            try:
                team = json.loads(str(team))
            except json.decoder.JSONDecodeError:
                team = str(team).replace(': " "', ': "')
                team = str(team).replace('"  "', '"')
                team = str(team).replace('": ",', '": " ",')
                team = json.loads(str(team))

            district_teams.append(team)

            data = [(int(team["teamNumber"]), team["nameShort"])]

            c.executemany("INSERT INTO entry_team(id,number,name) VALUES (NULL,?,?)", data)
            conn.commit()

    conn.commit()
    print("Done.")


def import_schedule():
    print("Importing Schedule...")

    c = conn.cursor()
    events = []

    for row in c.execute('SELECT * FROM entry_event WHERE id!=0'):
        events.append(row)

    for event in events:
        eventid = event[2]
        api_url = api_url_base + "/schedule/" + eventid + "/qual"
        response = requests.get(api_url, headers=header)
        FIRST_schedule = response.json()["Schedule"]

        try:
            FIRST_schedule[0]
        except IndexError:
            continue

        for match in FIRST_schedule:
            FIRST_teams = match["teams"]
            teams = []
            new_match = [()]

            for team in FIRST_teams:
                teams.append(team["teamNumber"])

            new_match[0] = (match["matchNumber"],
                            match["tournamentLevel"],
                            0,
                            0,
                            teams[0],
                            teams[1],
                            teams[2],
                            teams[3],
                            teams[4],
                            teams[5],
                            dbTools.event_id_lookup(eventid))

            sql = ''' INSERT INTO main.entry_schedule(match_number,match_type,blue_score,red_score,blue1,blue2,blue3,red1,red2,red3, event_id)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?) '''

            c.executemany(sql, new_match)
            conn.commit()

    print("Done.")


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
    item = item.replace('"Team 7509"', ' ')

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
    item = item.replace('O" Connor', "O' Connor")

    return str(item)


def get_date(string):
    string = str(string)[:10]
    strings = str(string).split('-')
    output = date(int(strings[0]), int(strings[1]), int(strings[2]))
    return output


# TODO Remove the force for flush
os.system('python3 manage.py flush --noinput')
import_events()
import_teams()
import_schedule()
