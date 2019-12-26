import tbaapiv3client as tba
from tbaapiv3client import ApiException
import sqlite3
import json
from apps.entry import config
import operator
import os

configuration = tba.Configuration()
configuration.api_key['X-TBA-Auth-Key'] = 'TaaEaU05CN3V89QGeDEKDSPYtfsFTAX0L8aNgAmjSAecJd2GpX4Avj5gQLjKKKls'


district_api = tba.DistrictApi(tba.ApiClient(configuration))
event_api = tba.EventApi(tba.ApiClient(configuration))
match_api = tba.MatchApi(tba.ApiClient(configuration))
district_key = config.current_district_key
event_key = config.current_event_key
event_data = []
district_teams = []
event_list = []


def change_district(new_district_key):
    global district_key
    district_key = new_district_key


def import_event(connection, event):
    c = connection.cursor()

    event = clean_request(event)

    print(" ")
    print(str(event))

    event = json.loads(event)
    event_data.append(event)

    data = [(str(event["name"]), str(event["key"]), str(event["event_type"]), get_date(event["start_date"]))]

    c.executemany("INSERT INTO entry_event VALUES (NULL,?,?,?,?,FALSE)", data)
    connection.commit()


def import_events():
    try:
        event_list = district_api.get_district_events_simple(district_key)
        # print(api_response)

        conn = sqlite3.connect("db.sqlite3")

        for event in event_list:
            import_event(conn, event)

        conn.close()
        print("\nDone")

    except ApiException as e:
        print("Exception when calling TBAApi->get_status: %s\n" % e)


def import_teams():
    try:
        team_list = district_api.get_district_teams_simple(config.current_district_key)

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
            c.executemany("INSERT INTO entry_team VALUES (NULL,?,?,?,0,0,0,0)", data)
            conn.commit()

            print(team)

    except ApiException as e:
        print("Exception when calling TBAApi->get_status: %s\n" % e)


def import_schedule():
    try:
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        events = []

        for row in c.execute('SELECT * FROM entry_event WHERE id!=0'):
            print(row)
            events.append(row)

        events.sort(key=operator.itemgetter(4))
        print(events)

        for event in events:
            c.execute('SELECT TBA_key FROM entry_event WHERE start=? AND imported=FALSE', (event[4],))
            event_key = c.fetchone()[0]
            data = [(True, event_key,)]
            c.execute('UPDATE entry_event SET imported = ? WHERE TBA_key = ?', data[0])
            conn.commit()

            teams = event_api.get_event_teams_simple(event_key)

            c.execute("SELECT id FROM entry_event WHERE TBA_key=?", (event_key,))
            event_id = c.fetchone()[0]

            for team in teams:

                cur_team = clean_request(team)

                first_remove = str(cur_team)[str(cur_team).find('name'):]
                second_replace = str(cur_team)[str(cur_team).find('nickname'):]

                cur_team = cur_team.replace(first_remove, '')
                cur_team = cur_team + second_replace

                cur_team = json.loads(cur_team)

                data = [(str(cur_team["key"]),)]
                data2 = [(event_id, cur_team["key"],)]
                print(data2)

                try:
                    c.execute('SELECT event_one_id FROM entry_team WHERE TBA_key=?', data[0])
                    if c.fetchone()[0] == 0:
                        c.execute('UPDATE entry_team SET event_one_id = ? WHERE TBA_key = ?', data2[0])
                        conn.commit()
                    else:
                        c.execute('SELECT event_two_id FROM entry_team WHERE TBA_key=?', data[0])
                        if c.fetchone()[0] == 0:
                            c.execute('UPDATE entry_team SET event_two_id = ? WHERE TBA_key=?', data2[0])
                            conn.commit()
                        else:
                            c.execute('SELECT event_three_id FROM entry_team WHERE TBA_key=?', data[0])
                            if c.fetchone()[0] == 0:
                                c.execute('UPDATE entry_team SET event_three_id = ? WHERE TBA_key=?', data2[0])
                                conn.commit()
                            else:
                                c.execute('SELECT event_four_id FROM entry_team WHERE TBA_key=?', data[0])
                                if c.fetchone()[0] == 0:
                                    c.execute('UPDATE entry_team SET event_four_id = ? WHERE TBA_key=?', data2[0])
                                    conn.commit()

                except TypeError as e:
                    e = 1

            event_matches = (event_api.get_event_matches_keys(event_key))

            for match_key in event_matches:
                print(match_key)

                match = json.loads(clean_request(match_api.get_match_simple(match_key)))

                c.execute("SELECT id FROM entry_event WHERE TBA_key=?", (match['event_key'],))

                match_type = match_key.split('_')[1]
                match_type = match_type.split('m')[0]
                if match_type.__contains__('qf'):
                    match_type = 200 + match['match_number']
                elif match_type.__contains__('sf'):
                    match_type = 300 + match['match_number']
                elif match_type.__contains__('q'):
                    match_type = 100 + match['match_number']
                elif match_type.__contains__('f'):
                    match_type = 400 + match['match_number']

                match_data = [((match['match_number']),
                               match_type,
                               match_key,
                               get_score(match, 0),  # Blue
                               get_score(match, 1),  # Red
                               get_teams(0, 0, match, c),   # Blue Team 1
                               get_teams(0, 1, match, c),   # Blue Team 2
                               get_teams(0, 2, match, c),   # Blue Team 3
                               event_id,
                               get_teams(1, 0, match, c),   # Red  Team 1
                               get_teams(1, 1, match, c),   # Red  Team 2
                               get_teams(1, 2, match, c)   # Red  Team 3
                               )]

                conn.commit()
                insert_schedule(conn, match_data)

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
            except IndexError as e:
                e = 1
        index += 1

    item = item.replace('"The Cybernauts"', ' ')

    return str(item)


def get_date(raw):

    raw = raw.replace(',', '')
    test = raw.split(" ")
    if len(test[1]) != 2:
        test[1] = '0' + test[1]
    if len(test[2]) != 2:
        test[2] = '0' + test[2]

    value = test[0] + test[1] + test[2]

    return value


def get_teams(alliance, place, match, c):
    # 0 for blue
    # 1 for red
    data = 0

    if alliance == 0:
        data = (str(match['alliances']['blue']['team_keys'][place]),)
    else:
        data = (str(match['alliances']['red']['team_keys'][place]),)
    c.execute('SELECT number FROM entry_team WHERE TBA_key=?', data)
    result = c.fetchone()
    try:
        return int(result[0])
    except TypeError:
        return 0


def get_score(match, alliance):
    # 0 for blue
    # 1 for red

    if alliance == 0:
        return match['alliances']['blue']['score']

    return match['alliances']['red']['score']


def full_reset():

    os.system('python3 manage.py flush')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO entry_event VALUES (0,0,0,0,0,FALSE)")
    conn.commit()
    c.execute("INSERT INTO entry_team VALUES (0,0,0,0,0,0,0,0)")
    conn.commit()
    c.execute("INSERT INTO entry_schedule VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0)")
    conn.commit()
    conn.close()


def insert_schedule(conn, match):
    """
    Create a new project into the projects table
    :param conn:
    :param match:
    """
    sql = ''' INSERT INTO main.entry_schedule(match_number,match_type,TBA_key,blue_score,red_score,blue1_id,blue2_id,blue3_id,event_id,red1_id,red2_id,red3_id)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, match)
    return


full_reset()
import_events()
import_teams()
import_schedule()
