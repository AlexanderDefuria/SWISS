import sqlite3

import requests
import json
import base64

from py import error

api_user = 'alexanderdefuria'
api_token = '75E35301-A10B-45BC-9453-396808B2E96C'
api_url_base = "https://frc-api.firstinspires.org/v2.0/"
b64_token = base64.b64encode((api_user + ':' + api_token).encode("utf-8"))

headers = {"Authorization": "Basic " + str(b64_token, "utf-8"),
           "Accept": "application/json"}

print(headers)

api_url = "https://frc-api.firstinspires.org/v2.0/2020/events?districtCode=ONT"
response = requests.get(api_url, headers=headers)

print("\n")


# print(response.json())

def import_event(connection, event):

        c = connection.cursor()

        event = clean_request(event)
        event = json.loads(event)
        data = [(str(event["name"]), str(event["code"]), str(event["type"]), str(event['dateStart']))]

        c.executemany("INSERT INTO main.entry_event VALUES (DEFAULT,?,?,?,?,FALSE)", data)

        print(data)





def import_events():

        event_list = response.json()['Events']

        conn = sqlite3.connect("db.sqlite3")

        for event in event_list:
            import_event(conn, event)

        conn.close()
        print("\nDone Event List")




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
                    item = item[:index] + '"' + item[index + 1:]
            except IndexError as e:
                e = 1
        index += 1

    item = item.replace('"The Cybernauts"', ' ')
    item = item.replace('"Team 7509"', '')

    item = item.replace('NA', '"NA"')
    item = item.replace('Thompson Recreation and Athletic Centre (TRAC" Western Road & Sarnia Road',
                        "Thompson Recreation and Athletic Centre (TRAC' Western Road & Sarnia Road")
    item = item.replace('Carleton University - Ravens" Nest',
                        "Carleton University - Ravens' Nest")


    return str(item)


import_events()
