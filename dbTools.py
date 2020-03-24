import sqlite3

conn = sqlite3.connect("db.sqlite3")

present_team_list = None


def team_id_lookup(team_number):
    """
    :param team_number: FRC Team Number
    :type team_number: int
    :return: Team ID within the DB
    """
    c = conn.cursor()
    c.execute("SELECT id FROM entry_team WHERE number==?", (team_number,))
    team_id = c.fetchone()[0]
    c.close()
    return team_id


def event_teams(event_key):
    """
    :param event_key: FIRST Event Key
    :type event_key: str
    :return : List of team IDs attending said event
    :rtype : List
    """
    global present_team_list

    if present_team_list is not None:
        return present_team_list

    match_list = []
    team_list = [0]
    c = conn.cursor()
    for row in c.execute('SELECT * FROM entry_schedule WHERE event_id==?', (event_key,)):
        match_list.append(row)

    for match in match_list:
        for index in range(3, 8):
            if not team_list.__contains__(match[index]):
                team_list.append(match[index])

    team_list.remove(0)
    team_list.sort()
    present_team_list = team_list
    return present_team_list


def update_event_teams(event_key):
    """
    :param event_key: FIRST Event Key
    :type event_key: str
    :return None
    """
    event_teams(event_key)


event_teams("ONBAR")
