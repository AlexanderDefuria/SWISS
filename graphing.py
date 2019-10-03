import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_teams_graph(form_data):

    print(pd.Series(form_data))

    team_list = []
    data_needed = []
    to_pop = []
    for x in form_data:
        form_data[x] = form_data[x][0]
        if form_data[x] == 'NaN' or form_data[x] == 'false':
            to_pop.append(x)
        elif 'team' in x:
            team_list.append(form_data[x])
        elif 'type' not in x:
            data_needed.append(x)

    for x in to_pop:
        form_data.pop(x)

    print(data_needed)

    df = pd.DataFrame({'Teams':team_list})

    print(df)

    get_data_from_db(data_needed, team_list)

    return


def get_data_from_db(data_needed, team_list):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    for x in data_needed:
        if x == 'totalHatches' or x == 'averageHatches':
            data_needed[x] = 'first_hatch'
            data_needed.append('second_hatch')
            data_needed.append('third_hatch')
        elif x == 'totalCargo' or x == 'averageCargo':
            data_needed[x] = 'first_cargo'
            data_needed.append('second_cargo')
            data_needed.append('third_cargo')
        elif x == 'totalDefense' or x == 'averageDefense':
            data_needed[x] = 'defense_time'

    compiled = dict.fromkeys(team_list, 1)

    for team in team_list:
        data = []

        c.execute("SELECT id FROM entry_team WHERE number=?", (int(team),))

        team_id = c.fetchall()

        for data_field in data_needed:

            if 'win' in data_field:
                continue

            c.executemany("SELECT ? FROM entry_match WHERE team_id=?", (data_field,int(team),))



    return
